from pprint import pprint
import requests
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

    def get_user_groups(self):      # Выводит все группы пользователя по его ID
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['extended'] = '1'
        params['fields'] = 'name'
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        print(f"У пользователя {response.json()['response']['count']} групп")
        for groupitem in response.json()['response']['items']:
            print(f"{groupitem['id']} ==> {groupitem['name']}")
            return groupitem['id']


    def get_group_members(self, groupid): # Возвращает список всех участников сообщества. Hо по фильтру только друзей
        params = self.get_params()
        params['group_id'] = groupid
        params['filter'] = 'friends'    # Возвращает только друзей. Если там их нет, то {'response': {'count': 0, 'items': []}}
        URL = 'https://api.vk.com/method/groups.getMembers'
        response = requests.get(URL, params)
        groups_dict = {"groupid": groupid, 'members_count': response.json()["response"]["count"]}
        print(f'Всего друзей в списке {response.json()["response"]["count"]}')
        print(response.json()['response']['items'])
        print(groups_dict)




Andrey = User(token, 'https://vk.com/ayakovtsev', 3293131)


# pprint(Andrey.user_friends_groups_lookup(11770))
# pprint(Andrey.get_user_groups())
# pprint(Andrey.get_friends(1000))

pprint(Andrey.get_group_members(Andrey.get_user_groups()))


