from TwitterAPI import TwitterAPI

from authlib.integrations.flask_client import OAuth
import os

CONSUMER_KEY = os.environ.get('API_KEY', None)
CONSUMER_SECRET = os.environ.get('API_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'prod'
WEBHOOK_URL = 'https://twitter2tg.onrender.com/webhook/twitter'

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, auth_type='oAuth1')

r = twitterAPI.request('account_activity/all/:prod/webhooks', {'url': WEBHOOK_URL})

print (r.status_code)
print (r.text)
