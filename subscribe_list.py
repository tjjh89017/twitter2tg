from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = os.environ.get('API_KEY', None)
CONSUMER_SECRET = os.environ.get('API_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

ENVNAME = os.environ.get('ENVNAME', 'prod')

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, auth_type='oAuth2')

r = twitterAPI.request('account_activity/all/:%s/subscriptions/list' %
                       ENVNAME, None, None, "GET")

#TODO: check possible status codes and convert to nice messages
print (r.status_code)
print (r.text)
