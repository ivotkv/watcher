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

from twilio.rest import Client as TwilioClient
from postmark import PMMail
from . import config

def send_sms(to, body):
    c = config.get('twilio')
    client = TwilioClient(c['account_sid'], c['auth_token'])
    client.api.account.messages.create(from_ = c['from'],
                                       to    = to,
                                       body  = body)

def send_email(to, subject, body):
    c = config.get('postmark')
    PMMail(api_key   = c['api_key'],
           sender    = c['from'],
           to        = to,
           subject   = subject,
           text_body = body).send()

def alert_all(subject, body, targets=None):
    if targets is None:
        targets = config.get('alert')
    if targets.get('email'):
        send_email(', '.join(targets['email']), subject, body)
    if targets.get('sms'):
        for sms in targets['sms']:
            send_sms(sms, subject)
