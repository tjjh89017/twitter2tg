#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask, request

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    # register webhook for twitter while startup
    # register webhook for telegram while startup
    app.run(debug=True)
