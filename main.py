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
import traceback
import time

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
        self.chat_id = -1001363258590
        self.backup_chat_id = -1001490525541

        self.api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.bot = telegram.Bot(TELEGRAM_TOKEN)

    def get_api(self):
        return self.api

    def get_bot(self):
        return self.bot

    def get_chat_id(self):
        return self.chat_id

    def get_backup_chat_id(self):
        return self.backup_chat_id

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
    print('responding to CRC call')

    return json.dumps(response)

@app.route('/webhook/twitter', methods=["POST"])
def webhook():
    global twitter2tg
    tg_bot = twitter2tg.get_bot()
    chat_id = twitter2tg.get_chat_id()
    backup_chat_id = twitter2tg.get_backup_chat_id()

    request_json = request.get_json()
    logger.info('test')
    #print(json.dumps(request_json, indent=2, sort_keys=True))

    favorite_events = request_json.get('favorite_events', [])
    for event in favorite_events:
        urls = set()
        urls.update([x['url'] for x in event['favorited_status']['entities'].get('urls', [])])
        urls.update([x['url'] for x in event['favorited_status']['entities'].get('media', [])])
        for url in urls:
            print(url)
            tg_bot.send_message(chat_id, url)
            tg_bot.send_message(backup_chat_id, url)

        extended_entities = event['favorited_status'].get('extended_entities', {})
        extended_tweet_extended_entities = event['favorited_status'].get('extended_tweet', {}).get('extended_entities', {})
        medias = extended_entities.get('media', []) + extended_tweet_extended_entities.get('media', [])
        photos = []
        videos = []
        for media in medias:
            try:
                if media['type'] == 'photo':
                    photos.append(media['media_url_https'] + "?name=large")
                elif media['type'] == 'video':
                    large_size_video = media['video_info']['variants'][0]
                    large_size_video['bitrate'] = 0
                    for x in media['video_info']['variants']:
                        if x.get('bitrate', 0) > large_size_video['bitrate']:
                            large_size_video = x
                    if large_size_video['content_type'] not in ['application/x-mpegURL']:
                        videos.append(large_size_video['url'])
            except Exception as e:
                traceback.print_exc()
                pass
        
        if len(photos) >= 1:
            temp_photos = [photos[x:x+10] for x in range(0, len(photos), 10)]
            for temp in temp_photos:
                try:
                    if len(temp) == 1:
                        tg_bot.send_photo(backup_chat_id, temp[0])
                        #tg_bot.send_document(backup_chat_id, temp[0])
                    else:
                        temp_media = [telegram.InputMediaPhoto(x) for x in temp]
                        tg_bot.send_media_group(backup_chat_id, temp_media, timeout=1000)

                        #temp_media = [telegram.InputMediaDocument(x) for x in temp]
                        #tg_bot.send_media_group(backup_chat_id, temp_media, timeout=1000)
                except Exception as e:
                    traceback.print_exc()
                    pass

        if len(videos) >= 1:
            temp_videos = [videos[x:x+10] for x in range(0, len(videos), 10)]
            for temp in temp_videos:
                try:
                    if len(temp) == 1:
                        tg_bot.send_document(backup_chat_id, temp[0])
                    else:
                        temp_media = [telegram.InputMediaDocument(x) for x in temp]
                        tg_bot.send_media_group(backup_chat_id, temp_media, timeout=1000)
                except Exception as e:
                    traceback.print_exc()
                    pass
        
    return ('', HTTPStatus.OK)

# register webhook for twitter while startup
# register telegram while startup
twitter2tg = Twitter2tg()

if __name__ == '__main__':
    app.run(debug=True)
