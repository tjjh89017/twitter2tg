from TwitterAPI import TwitterAPI

import os
import json

CONSUMER_KEY = os.environ.get('API_KEY', None)
CONSUMER_SECRET = os.environ.get('API_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'prod'

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, auth_type='oAuth2')

#r = twitterAPI.request('account_activity/all/:%s/webhooks' % ENVNAME, {'url': WEBHOOK_URL})

r = twitterAPI.request('account_activity/all/webhooks')
j = json.loads(r.text)

r = twitterAPI.request('account_activity/all/:prod/webhooks/:{}'.format(j['environments'][0]['webhooks'][0]['id']))

print (r.status_code)
print (r.text)
