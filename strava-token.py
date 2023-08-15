import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

# Initial Settings
client_id = 46109
client_secret = config.get('STRAVA_CLIENT_SECRET')
redirect_uri = 'http://localhost/'

# Authorization URL
request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

# User prompt showing the Authorization URL asking for the code
print('Click here:', request_url)
print('Please authorize the app and copy/paste the generated code in the URL below')
code = input('Paste the code from the URL: ')

# Get the access token
token = requests.post(
    url='https://www.strava.com/api/v3/oauth/token',
    data= {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
        })

#print token in a variable
strava_token = token.json()
print('strava_token to replace in .env', strava_token['access_token'])