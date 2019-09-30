#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import logging
import json
import requests
import hmac
import hashlib
import base64

from http import HTTPStatus
from flask import Flask, request
from TwitterAPI import TwitterAPI

import telegram

API_KEY = os.environ.get('API_KEY', None)
API_SECRET = os.environ.get('API_SECRET', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', None)

# Enable logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class Twitter2tg():
    def __init__(self):
        self.api = None
        self.url = 'https://twitter2tg.herokuapp.com/webhook/twitter/'

        self.api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.bot = telegram.Bot(TELEGRAM_TOKEN)

    def get_api(self):
        return self.api

    def get_bot(self):
        return self.bot

    def deinit(self):
        pass

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/webhook/twitter', methods=["GET"])
def webhook_crc():
    crc = request.args['crc_token']

    validation = hmac.new(
        key=bytes(API_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    #print('responding to CRC call')

    return json.dumps(response)

@app.route('/webhook/twitter', methods=["POST"])
def webhook():
    global twitter2tg
    tg_bot = twitter2tg.get_bot()

    request_json = request.get_json()
    logger.info('test')
    #print(json.dumps(request_json, indent=2, sort_keys=True))

    favorite_events = request_json.get('favorite_events', [])
    for event in favorite_events:
        urls = set()
        urls.update([x['url'] for x in event['favorited_status']['entities'].get('urls', [])])
        urls.update([x['url'] for x in event['favorited_status']['entities'].get('media', [])])
        for url in urls:
            tg_bot.send_message(-1001347068882, url)

    return ('', HTTPStatus.OK)

# register webhook for twitter while startup
# register telegram while startup
twitter2tg = Twitter2tg()

if __name__ == '__main__':
    app.run(debug=True)
