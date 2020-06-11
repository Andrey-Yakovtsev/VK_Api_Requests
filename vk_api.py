from pprint import pprint
import requests
from urllib.parse import urlencode
import json


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '65193ed9703c93e114e9d94176976acddaaf57d7df53b15361c09602856f82192dbe23bf39f05c6c16f17'
OAUTH_PARAMS = {
    'client_id': '7493907', #ID  приложения которое просит доступ
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.89
}

print('?'.join(
    (OAUTH_URL, urlencode(OAUTH_PARAMS))
))

class User:
    def __init__(self, token, owner_id: int):
        self.token = token
        self.owner_id = int(owner_id) # ID юзера в ВК


    def get_params(self):
        return {
            'access_token': token,
            'v': 5.89,
        }


    def get_friends(self, count): # Выводит все друзей пользователя по его ID
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['count'] = count #  кол-во друзей в выводе (умолч. - 5000)
        params['fields'] = 'nickname', 'domain'
        URL = 'https://api.vk.com/method/friends.get'
        response = requests.get(URL, params)
        friends_list = []
        for item in response.json()['response']['items']:
            friends_list.append(item['id'])
        return print('Список друзей', friends_list)

    def __and__(self, friend):
        params = self.get_params()
        params['source_uid'] = self.owner_id     # с каким пользователем сравниваем
        params['target_uids'] = friend.owner_id     # каких пользователей сравниваем
        URL = 'https://api.vk.com/method/friends.getMutual'
        response = requests.get(URL, params)
        for item in response.json()['response']:
            return item['common_friends'] #item['common_friends'],


Andrey = User(token, 3293131)
Genka = User(token, 3730376)
Sofya = User(token, 268721993)
Yana = User(token, 4867400)



a_s_list = Andrey & Sofya
a_y_list = Andrey & Yana
a_g_list = Andrey & Genka

print(f'У пользователей Andrey и Sofya  {len(a_s_list)} общих друзей')
print(f'У пользователей Andrey и Yana  {len(a_y_list)} общих друзей')
print(f'У пользователей Andrey и Genka  {len(a_g_list)} общих друзей')


