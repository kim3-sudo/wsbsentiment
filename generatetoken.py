import requests
from decouple import config

auth = requests.auth.HTTPBasicAuth(config('REDDIT_CLIENT_API'), config('REDDIT_API_SECRET'))
data = {'grant_type': 'password',
        'username': config('REDDIT_USERNAME'),
        'password': config('REDDIT_PASSWORD')}
headers = {'User-Agent': 'Python:wsbsentiment:v0.0.9002 (by /u/kim3-sudo)'}
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

TOKEN = response.json()['access_token']
print(TOKEN)

file = open("./token", "w")
file.write(TOKEN)
file.close()