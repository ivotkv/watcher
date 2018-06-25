# -*- coding: utf-8 -*-
# 
# The MIT License (MIT)
# 
# Copyright (c) 2018 Ivo Tzvetkov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

from __future__ import print_function, unicode_literals, absolute_import

from time import sleep
from pytz import timezone
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from .helpers.alerts import alert_all
from .helpers import config

SUBJECT = """
DATA FRESHNESS: {0}
""".strip()

BODY = """
There have been no {0} events in the last {1} minutes.

Last event received: {2}
""".strip()

class Watcher(object):

    def __init__(self):
        self.config = {}
        for name, cfg in config.get('watchers')['data_freshness'].iteritems():
            url = "{0}://{1}:{2}@{3}/{4}".format(cfg['type'],
                                                 cfg['user'],
                                                 cfg['pass'],
                                                 cfg['host'],
                                                 cfg['database'])
            table = '{0}.{1}'.format(cfg['schema'], cfg['table']) if cfg['schema'] else cfg['table']
            self.config[name] = {
                'engine': create_engine(url, pool_recycle=3600),
                'query': "select {0} from {1} order by {2} desc limit 1".format(cfg['date_field'],
                                                                                cfg['table'],
                                                                                cfg['sort_field']),
                'date_tz': timezone(cfg['date_tz']),
                'threshold': cfg['threshold'],
                'silent_from': cfg.get('silent_from'),
                'silent_until': cfg.get('silent_until'),
                'silent_weekends': bool(cfg.get('silent_weekends')),
                'silent_tz': timezone(cfg['silent_tz']) if cfg.get('silent_tz') else timezone(cfg['date_tz']),
                'alert': cfg.get('alert')
            }
        self.alerts = {}

    def run(self):
        while True:
            for name, cfg in self.config.iteritems():
                # check whether to silence
                now = datetime.now(cfg['silent_tz'])
                if cfg['silent_weekends'] and now.isoweekday() > 5:
                    continue
                if cfg['silent_from'] is not None and cfg['silent_until'] is not None:
                    if cfg['silent_from'] < cfg['silent_until']:
                        if cfg['silent_from'] <= now.hour < cfg['silent_until']:
                            continue
                    else:
                        if cfg['silent_from'] <= now.hour or now.hour < cfg['silent_until']:
                            continue

                # fetch and check latest date
                now = datetime.now(cfg['date_tz'])
                with cfg['engine'].connect() as conn:
                    latest = cfg['date_tz'].localize(conn.execute(cfg['query']).fetchall()[0][0])
                if now - latest > timedelta(minutes=cfg['threshold']):
                    if name not in self.alerts or now - self.alerts[name] > timedelta(seconds=300):
                        alert_all(SUBJECT.format(name), BODY.format(name, cfg['threshold'], latest), targets=cfg['alert'])
                        self.alerts[name] = now

            sleep(60)
