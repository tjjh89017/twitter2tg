#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask, request

import os
import logging
import json
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class Twitter():
    def __init__(self):
        self.id = None
        self.url = 'https://twitter2tg.herokuapp.com/webhook/twitter/'
        self.bearer_token = None

        r = requests.post('https://api.twitter.com/oauth2/token', auth=(os.environ['API_KEY'], os.environ['API_SECRET']))
        if r.status_code == requests.codes.ok:
            logger.info(r.text)
            print(r.text)
            self.bearer_token = json.loads(r.text)['access_token']

        param = {'url': self.url}
        header = {'authorization:': 'OAuth oauth_consumer_key="{}", oauth_nonce="GENERATED", oauth_signature="GENERATED", oauth_signature_method="HMAC-SHA1", oauth_timestamp="GENERATED", oauth_token="{}", oauth_version="1.0"'.format(os.environ['API_KEY'], os.environ['ACCESS_TOKEN'])}
        r = requests.post('https://api.twitter.com/1.1/account_activity/all/dev/webhooks.json', param=param, header=header)
        if r.status_code == requests.codes.ok:
            logger.info(r.text)
            print(r.text)
            j = json.loads(r.text)
            self.id = j.id

        # check status of webhook
        header = {'authorization:': 'Bearer {}'.format(self.bearer_token)}
        r = requests.post('https://api.twitter.com/1.1/account_activity/all/dev/webhooks.json', param=param, header=header)
        if r.status_code == requests.codes.ok:
            logger.info(r.text)
            print(r.text)
        
        # TODO Testing
        header = {'authorization:': 'OAuth oauth_consumer_key="{}", oauth_nonce="GENERATED", oauth_signature="GENERATED", oauth_signature_method="HMAC-SHA1", oauth_timestamp="GENERATED", oauth_token="{}", oauth_version="1.0"'.format(os.environ['API_KEY'], os.environ['ACCESS_TOKEN'])}
        r = requests.post('https://api.twitter.com/1.1/account_activity/all/dev/webhooks/{}.json'.format(self.id), header=header)

    def deinit(self):
        pass

@app.route('/')
def index():
    return 'Hello World!'

#app.route('/webhook/twitter')
def webhook_twitter():
    pass

if __name__ == '__main__':
    # register webhook for twitter while startup
    twitter = Twitter()
    # register webhook for telegram while startup
    app.run(debug=True)
