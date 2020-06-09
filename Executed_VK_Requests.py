from pprint import pprint
import requests
import json
import time


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = 'c5d80011754c61be9e5c14046c4c3fdc47a79be0f1834ace23ca1264e05fb0241ef45c68494356c568fb5'
OAUTH_PARAMS = {
    'client_id': '7493907', #ID  приложения которое просит доступ
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.89
}

version = 5.89
owner_id = '3293131'

domain = 'https://vk.com/ayakovtsev'

import requests

API = "https://api.vk.com/method"
ACCESS_TOKEN = "65193ed9703c93e114e9d94176976acddaaf57d7df53b15361c09602856f82192dbe23bf39f05c6c16f17"
V = '5.89'

response = requests.post(url=f"{API}/execute",
                         data={
                             "code": "var members = API.users.getFollowers({\"user_id\": \"3293131\"})"
                                     "var count = 1000;"
                                     "return members;",
                             "access_token": ACCESS_TOKEN,
                             "v": V,
                         })

pprint(response.text)


"""

class User:
    def __init__(self, token, owner_id: int):
        self.token = token
        self.owner_id = int(owner_id) # ID юзера в ВК

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.89,
        }

    def get_user_groups(self):
        '''
        :return: Выводит все группы пользователя по его ID
        '''
        groups_ids_list = []
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['extended'] = '1'
        params['fields'] = 'name', 'members_count'
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        print(f"У пользователя всего {response.json()['response']['count']} групп")
        global groups_ids_names_dict
        groups_ids_names_dict = {}
        global groups_ids_usercount_dict
        groups_ids_usercount_dict = {}
        for groupitem in response.json()['response']['items']:
            if groupitem.get('deactivated') == 'banned':
                print(f' Из них группа {groupitem["id"]} забанена и не добавлена в список')
            else:
                groups_ids_names_dict.update({groupitem['id']: groupitem['name']})  # Собрал словарь из Айди - Имя, чтоб потом подтянуть в файл
                groups_ids_usercount_dict.update({groupitem['id']: groupitem['members_count']})  # Собрал словарь из Айди - кол-во юзеров, чтоб потом подтянуть в файл
                groups_ids_list.append(groupitem['id'])  # Собрал список всех ID своих групп, чтобы потом по ним пройтись
        return groups_ids_list


    def get_group_members(self, groupid):
        '''
        :param groupid: принимает идентификатор группы
        :return: Возвращает список всех участников сообщества. По 'filter'='friend' возвращает только друзей
        '''
        params = self.get_params()
        params['group_id'] = groupid
        params['filter'] = 'friends'    # Возвращает только друзей. Если там их нет, то {'response': {'count': 0, 'items': []}}
        URL = 'https://api.vk.com/method/groups.getMembers'
        response = requests.get(URL, params)
        if response.json()["response"]["count"] == 0:
            groups_dict = {
                "groupid": groupid,
                "groupname": groups_ids_names_dict[groupid],
                'members_count': groups_ids_usercount_dict[groupid]
            }
            return groups_dict
        else:
            return None


Andrey = User(token, 3293131)

if __name__ == '__main__':
    with open('groups.json', 'w', encoding='utf-8') as fileoutput:
        json_list = []
        for unique_id in Andrey.get_user_groups():
            print('Requesting  VK API...')
            data = Andrey.get_group_members(unique_id)
            time.sleep(1)
            if data:
                json_list.append(data)
                pprint(data)
        json.dump(json_list, fileoutput, ensure_ascii=False, indent=4)


"""