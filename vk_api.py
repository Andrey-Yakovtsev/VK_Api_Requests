from pprint import pprint
import requests
from urllib.parse import urlencode
import json


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '6f7d6851625a2ed32a699df5d3188f43810a3876951821c01991ea59730e3a6092bac5d02da393fd1e9a8'
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
    def __init__(self, token, owner_id: int): #domain,
        self.token = token
        # self.domain = 'domain'
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

    def get_mutual_friends(self, *friends):
        params = self.get_params()
        params['source_uid'] = self.owner_id     # с каким пользователем сравниваем
        params['target_uids'] = friends     # каких пользователей сравниваем
        URL = 'https://api.vk.com/method/friends.getMutual'
        response = requests.get(URL, params)
        # print(response.json()['response'])
        # print(len(response.json()['common_count']))
        for item in response.json()['response']:
            return len(item['common_friends']) #item['common_friends'],
    #
    # def get_user_groups(self):      # Выводит все группы пользователя по его ID
    #     params = self.get_params()
    #     params['user_id'] = self.owner_id
    #     params['extended'] = '1'
    #     params['fields'] = 'name' #,'deactivated','is_closed'
    #     URL = 'https://api.vk.com/method/groups.get'
    #     response = requests.get(URL, params)
    #     print(response.text)
    #     print(f"У пользователя {response.json()['response']['count']} групп")
    #     for groupitem in response.json()['response']['items']:
    #         print(f"{groupitem['id']} ==> {groupitem['name']}")
    #         return groupitem['id']
    #
    #
    # def user_friends_groups_lookup(self, groupid): # Выводит список друзей по ID группы
    #     params = self.get_params()
    #     params['user_ids'] = str(self.get_friends(1000))
    #     # params['extended'] = 1
    #     params['group_id'] = groupid
    #     URL = 'https://api.vk.com/method/groups.isMember'
    #     response = requests.get(URL, params)
    #     i = 0
    #     for item in  (response.json()['response']):
    #         if item['member'] == 1:
    #             i+=1
    #             print(i, '==>', item['user_id'])

    # def get_group_members(self, groupid): # Возвращает список всех участников сообщества. Hо по фильтру только друзей
    #     params = self.get_params()
    #     params['group_id'] = groupid
    #     # params['fields'] = 'common_count'
    #     params['filter'] = 'friends'    # Возвращает только друзей. Если там их нет, то {'response': {'count': 0, 'items': []}}
    #     URL = 'https://api.vk.com/method/groups.getMembers'
    #     response = requests.get(URL, params)
    #     groups_dict = {"groupid": groupid, 'members_count': response.json()["response"]["count"]}
    #     print(f'Всего друзей в списке {response.json()["response"]["count"]}')
    #     print(response.json()['response']['items'])
    #     print(groups_dict)




Andrey = User(token, 3293131)
Genka = User(token, 3730376)
Sofya = User(token, 268721993)
Yana = User(token, 4867400)


# pprint(Andrey.user_friends_groups_lookup(11770))
# pprint(Andrey.get_user_groups())
# pprint(Andrey.get_friends(1000))
pprint(Andrey.get_mutual_friends(3730376 and 4867400 and 268721993))
# pprint(Andrey.get_group_members(11770))

