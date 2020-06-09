from pprint import pprint
import requests
import json
import time


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '65193ed9703c93e114e9d94176976acddaaf57d7df53b15361c09602856f82192dbe23bf39f05c6c16f17'
OAUTH_PARAMS = {
    'client_id': '7493907', #ID  приложения которое просит доступ
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.89
}




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
        Предлагаю возвращать из get_user_groups не просто список групп,
        а следующую структуру: {group_id: {'members_count: ..., 'name':...}
        '''
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['extended'] = '1'
        params['fields'] = 'name', 'members_count'
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        groups_ids_names_dict = {}
        for groupitem in response.json()['response']['items']:
            if not groupitem.get('deactivated') == 'banned':
                groups_ids_names_dict.update(
                    {groupitem['id']:
                         {'members_count': groupitem['members_count'], 'name': groupitem['name']}
                     }
                )  # Собрал словарь из Айди - Имя, чтоб потом подтянуть в файл
            else:
                print(f' Группа {groupitem["id"]} забанена и не добавлена в список')
        return groups_ids_names_dict



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
        return response.json()



Andrey = User(token, 3293131)

common_friends_groups_dict = {}
to_json_file_list = []
for keys, values in Andrey.get_user_groups().items():
    if Andrey.get_group_members(keys)['response']['count'] != 0:
        common_friends_groups_dict = {'groupid': keys,
                         'groupname': values['name'],
                         'members_count': values['members_count']}
    else:
        continue
    to_json_file_list.append(common_friends_groups_dict)
    time.sleep(0.5)
    print('Requesting  VK API. Collectig data for JSON file')



if __name__ == '__main__':
    with open('groups.json', 'w', encoding='utf-8') as fileoutput:
        json.dump(to_json_file_list, fileoutput, ensure_ascii=False, indent=4)

