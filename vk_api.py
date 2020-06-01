from pprint import pprint
import requests
from urllib.parse import urlencode
import json


OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMS = {
    'client_id': '7493907',
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.89
}

# print('?'.join(
#     (OAUTH_URL, urlencode(OAUTH_PARAMS))
# ))
token = '500bea61bc2aeb0f830121cb5f91dc73ff9e2e40ef58771cbfd6f3a1c0e77666f7067702661070939c376'
params = {
    'access_token': token,
    'v': 5.89,
    'owner_id': '3293131', #integer
    'domain': 'https://vk.com/ayakovtsev',
    'count': 10
}

#
# pprint()

#
# pprint(response.json())

# ' #получаем список постов на стере
#
#

class User:
    def __init__(self, token, domain, owner_id: int):
        self.token = token
        self.domain = 'domain'
        self.owner_id = int(owner_id)

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.89,
        }
    def get_status(self):
        params = self.get_params()
        URL = 'https://api.vk.com/method/status.get'
        response = requests.get(URL, params)
        return response.json()['response']['text']

    def set_status(self, text):
        params = self.get_params()
        params['text'] = text
        URL = 'https://api.vk.com/method/status.set'
        response = requests.get(URL, params)
        return response.json()['response']

    def get_wall_messages(self):
        params = self.get_params()
        params['domain'] = self.domain
        params['owner_id'] = self.owner_id
        URL = 'https://api.vk.com/method/wall.get'
        response = requests.get(URL, params)
        for item in response.json()['response']['items']:
             return print(item['text'])



Andrey = User(token, 'https://vk.com/ayakovtsev', 3293131)

print(Andrey.get_wall_messages())
