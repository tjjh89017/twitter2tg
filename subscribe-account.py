from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = os.environ.get('API_KEY', None)
CONSUMER_SECRET = os.environ.get('API_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

ENVNAME = os.environ.get('ENVNAME', 'dev')

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/subscriptions' %
                       ENVNAME, None, None, "POST")

#TODO: check possible status codes and convert to nice messages
print (r.status_code)
