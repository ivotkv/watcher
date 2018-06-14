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

import subprocess
from subprocess import CalledProcessError
from time import sleep
from datetime import datetime, timedelta
from .helpers.alerts import alert_all
from .helpers import config

SUBJECT = """
SSH CHECK: Failed: {0}
""".strip()

BODY = """
SSH check failed for: {0}

The following command failed:

{1}

--

An alert is triggered if the comand exits non-zero or the output is blank.

Good luck!
""".strip()

class Watcher(object):

    def __init__(self):
        self.config = config.get('watchers')['ssh_check']
        self.alerts = {}

    def run(self):
        while True:
            now = datetime.now()
            for name, cfg in self.config.iteritems():
                ssh = ['ssh', '{0}@{1}'.format(cfg['user'], cfg['host']), '-i', cfg['key']]
                for command in cfg['commands']:
                    try:
                        assert subprocess.check_output(ssh + command).strip()
                    except (AssertionError, CalledProcessError):
                        if name not in self.alerts or now - self.alerts[name] > timedelta(seconds=300):
                            alert_all(SUBJECT.format(name), BODY.format(name, ' '.join(command)), targets=cfg.get('alert'))
                            self.alerts[name] = now
                        break
            sleep(60)
