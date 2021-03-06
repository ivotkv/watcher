#!/usr/bin/env python
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

import os
import sys
import traceback
from time import sleep
from argparse import ArgumentParser
from watchers.helpers.alerts import alert_all

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

args = ArgumentParser()
args.add_argument("--debug", action="store_true", default=False)
args.add_argument("watcher", type=str)
args = args.parse_args()

module = __import__('watchers.{0}'.format(args.watcher), globals(), locals(), ['Watcher'], 0)
try:
    module.Watcher().run()
except KeyboardInterrupt:
    pass
except:
    if not args.debug:
        alert_all('WATCHER ERROR: {0}'.format(args.watcher), ''.join(traceback.format_exception(*sys.exc_info())))
        sleep(300)
    raise
