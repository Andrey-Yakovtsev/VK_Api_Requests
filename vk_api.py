from pprint import pprint
import requests
from urllib.parse import urlencode
import json


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '500bea61bc2aeb0f830121cb5f91dc73ff9e2e40ef58771cbfd6f3a1c0e77666f7067702661070939c376'
OAUTH_PARAMS = {
    'client_id': '7493907', #ID  приложения которое просит доступ
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.89
}

class User:
    def __init__(self, token, domain, owner_id: int):
        self.token = token
        self.domain = 'domain'
        self.owner_id = int(owner_id) # ID юзера в ВК

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.89,
        }
    # def get_status(self):
    #     params = self.get_params()
    #     URL = 'https://api.vk.com/method/status.get'
    #     response = requests.get(URL, params)
    #     return response.json()['response']['text']
    #
    # def set_status(self, text):
    #     params = self.get_params()
    #     params['text'] = text
    #     URL = 'https://api.vk.com/method/status.set'
    #     response = requests.get(URL, params)
    #     return response.json()['response']

    # def get_wall_messages(self, counter):
    #     params = self.get_params()
    #     params['domain'] = self.domain
    #     params['owner_id'] = self.owner_id
    #     params['count'] = counter
    #     URL = 'https://api.vk.com/method/wall.get'
    #     response = requests.get(URL, params)
    #     for item in response.json()['response']['items']:
    #          print(item['text'])

    def get_friends(self, count):
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['count'] = count #  кол-во друзей в выводе (умолч. - 5000)
        params['fields'] = 'nickname', 'domain'
        URL = 'https://api.vk.com/method/friends.get'
        response = requests.get(URL, params)
        friends_list = []
        for item in response.json()['response']['items']:
            friends_list.append(item['id'])
        return friends_list
    # def get_mutual_friends(self, friend1, friend2):
    #     params = self.get_params()
    #     # user1 = self.owner_id
    #     # user2 = self.owner_id
    #     params['source_uid'] = self.owner_id     # с каким пользователем сравниваем
    #     params['target_uids'] = [friend1.owner_id, friend2.owner_id]     # какого пользователя сравниваем
    #     URL = 'https://api.vk.com/method/friends.getMutual'
    #     response = requests.get(URL, params)
    #     for item in response.json()['response']:
    #         return item['common_friends'], len(item['common_friends'])

    def get_user_groups(self):
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['extend'] = 1
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        print(response.json()['response'])


    # def user_friends_groups_lookup(self, groupid):
    #     params = self.get_params()
    #     params['user_ids'] = self.get_friends(5)
    #     params['extended'] = 1
    #     params['group_id'] = groupid
    #     URL = 'https://api.vk.com/method/groups.isMember'
    #     response = requests.get(URL, params)
    #     print(response.json())

    def get_group_members(self, groupid): # Возвращает список участников сообщества.
        params = self.get_params()
        params['group_id'] = groupid
        # params['fields'] = 'common_count'
        params['filter'] = 'friends'    # Возвращает только друзей. Если там их нет, то {'response': {'count': 0, 'items': []}}
        URL = 'https://api.vk.com/method/groups.getMembers'
        response = requests.get(URL, params)
        print(response.json())



Andrey = User(token, 'https://vk.com/ayakovtsev', 3293131)
Genka = User(token, 'https://vk.com/id3730376', 3730376)
Sofya = User(token, 'https://vk.com/s.yakovtseva', 268721993)
Yana = User(token, 'https://vk.com/id4867400', 4867400)


# pprint(Andrey.user_friends_groups_lookup(90329578))
# pprint(Andrey.get_user_groups())
# pprint(Andrey.get_friends(10))

pprint(Andrey.get_group_members(44016898))


