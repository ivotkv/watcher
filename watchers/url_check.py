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

import re
import requests
from time import sleep
from datetime import datetime, timedelta
from .helpers.alerts import alert_all
from .helpers import config

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0 Safari/537.36'

SUBJECT = """
URL CHECK: Failed: {0}
""".strip()

BODY = """
URL check failed for: {0}

HTTP Status Code: {1}
HTTP Text: {2}
Latency: {3} ms

--

An alert is triggered if:

{4}

Verify the associated application and that the above URL responds correctly.

Good luck!
""".strip()

class Watcher(object):

    def __init__(self):
        self.config = config.get('watchers')['url_check']
        self.alerts = {}

    def run(self):
        while True:
            now = datetime.now()
            for url, opts in self.config.iteritems():
                headers = {
                    'user-agent': opts['user_agent'] if 'user_agent' in opts else USER_AGENT
                }
                r = requests.get(url, headers=headers)
                ms = r.elapsed.microseconds / 1000
                conds = ["- The HTTP code is not 200"]
                ok = r.status_code == 200
                if 'response' in opts:
                    conds.append("- The response doesn't match '{0}'".format(opts['response']))
                    ok = ok and re.search(opts['response'], r.text)
                if 'latency' in opts:
                    conds.append("- The latency exceeds {0} ms".format(opts['latency']))
                    ok = ok and ms < opts['latency']
                if not ok:
                    if url not in self.alerts or now - self.alerts[url] > timedelta(seconds=300):
                        alert_all(SUBJECT.format(url), BODY.format(url, r.status_code, r.text, ms, '\n'.join(conds)))
                        self.alerts[url] = now
            sleep(60)
