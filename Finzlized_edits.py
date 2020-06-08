from pprint import pprint
import requests
import json
import time


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '187ac7919b1156d715de5b9549df042085c17561bdfbea8c42c5b31d9222098332a50a66b1360bb5b4841'
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
        groups_ids_list = []
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['extended'] = '1'
        params['fields'] = 'name', 'members_count'
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        groups_idfinal_dicts_names_dict = {}
        for groupitem in response.json()['response']['items']:
            if not groupitem.get('deactivated') == 'banned':
                # groups_ids_names_dict.update(
                #     {groupitem['id']:
                #          {'members_count':groupitem['members_count'], 'name': groupitem['name']}
                #      }
                # )  # Собрал словарь из Айди - Имя, чтоб потом подтянуть в файл
                groups_ids_list.append(
                    {groupitem['id']:
                         {'members_count': groupitem['members_count'], 'name': groupitem['name']}
                     }
                )
            else:
                print(f' Из них группа {groupitem["id"]} забанена и не добавлена в список')
        pprint(groups_ids_list)
        # pprint(groups_ids_names_dict)
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
        # pprint(response.text)
        return response.json()

Andrey = User(token, 3293131)
common_friends_groups_dict = {}
for group_id in Andrey.get_user_groups():
    if Andrey.get_group_members(group_id)['response']['count'] != 0:

        common_friends_groups_dict.update({'groupid': group_id}) 

print(common_friends_groups_dict)




# Andrey.get_user_groups()
# Andrey.get_group_members(66319524)
# if __name__ == '__main__':
#     with open('groups.json', 'w', encoding='utf-8') as fileoutput:
#         json_list = []
#         for unique_id in Andrey.get_user_groups():
#             print('Requesting  VK API...')
#             data = Andrey.get_group_members(unique_id)
#             time.sleep(1)
#             if data:
#                 json_list.append(data)
#                 pprint(data)
#         json.dump(json_list, fileoutput, ensure_ascii=False, indent=4)


