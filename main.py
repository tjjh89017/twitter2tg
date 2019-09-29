#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import logging
import json
import requests
import hmac
import hashlib
import threading
import time

from http import HTTPStatus
from flask import Flask, request
from TwitterAPI import TwitterAPI

API_KEY = os.environ.get('API_KEY', None)
API_SECRET = os.environ.get('API_SECRET', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)


# Enable logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class Twitter():
    def __init__(self):
        self.api = None
        self.url = 'https://twitter2tg.herokuapp.com/webhook/twitter/'

        self.api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def start_webhook(self):
        # init webhook
        r = self.api.request('account_activity/all/:dev/webhooks', {'url': self.url})
        logger.info("init webhook")
        logger.info(r.status_code)
        logger.info(r.text)

        # check webhook
        r = self.api.request('account_activity/all/webhooks')
        logger.info(r.status_code)
        logger.info(r.text)

    def get_api(self):
        return self.api

    def deinit(self):
        pass

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/webhook/twitter', methods=["GET"])
def webhook_crc():
    crc = request.args['crc_token']

    validation = hmac.new(
        key=bytes(CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')

    return json.dumps(response)

@app.route('/webhook/twitter', methods=["POST"])
def webhook():
    request_json = request.get_json()
    print(json.dumps(request_json, indent=4, sort_keys=True))

    return ('', HTTPStatus.OK)

def start_webhook(api):
    time.sleep(10)
    api.start_webhook()

if __name__ == '__main__':
    # register webhook for twitter while startup
    twitter = Twitter()
    threading.Thread(target=start_webhook, args=(twitter,))
    # register webhook for telegram while startup
    app.run(debug=True)
