'''
1. Какие классы кроме USER еще могут пригодиться?  DB_OBJECT?
2. БД - какую взять?


Последовательности:
1. Берем какого-то юзера (ID/Name)
2. Собираем его данные (пол, семейное положение (эти 2 параметра в отдельные таблички БД, для ускорения фильтрации)
 возраст(что делать с 18-), город, интересы(2-й этап))

3. Получаем список подходящих из 1000 (как обойти ограничение? и как сразу выкидывать малолетних и семейных?)
4. Фильтруем и сортируем по интересам
    (Веса: общий город - 50%,
    близкий возраст (или одинаковый) - 30%,
    наличие общих интересов - 20%
4.9 Проверяем наличие результатов в базе результатов (п.6) - выкидываем совпадения.
5. Выводим ТОР -10 в Джейсон. Можно имя файла обновлять, чтобы хранить результаты всех запросов.
6. Пишем вывод в БД результатов
'''

from pprint import pprint
import requests
import json
import time


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '75f6907e1aa79fed1222227787c392b151eed6eaec6c6edf20429648a6fd40eff4d001121b560aaa223fa'
OAUTH_PARAMS = {
    'client_id': '7493907', #ID  приложения которое просит доступ
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups, offline',
    'response_type': 'token',
    'v': 5.89
}
# ID user от которого прошла строка 189983982

def get_params():
    return {
        'access_token': token,
        'v': 5.89,
    }

class CommonMethods:
    def __init__(self, token):
        self.token = token

    def user_search(self, search_query: str):
        params = get_params()
        params['q'] = search_query
        # params['user_id'] = owner_id # Здесь не используется
        # params['count'] = count  # кол-во записей в выводе (умолч. - 1000)
        params['has_photo'] = 1 # без фотки не выводятся
        params['fields'] = 'nickname', 'photo_id', 'verified', 'sex', 'bdate', 'city', 'country', \
                           'home_town', 'has_photo',  'photo_max', 'photo_max_orig', 'domain', \
                           'has_mobile', 'contacts', 'common_count', 'nickname', 'interests', 'screen_name'
        URL = 'https://api.vk.com/method/users.search'
        response = requests.get(URL, params)
        results_list = []
        print(response.text)
        for item in response.json()['response']['items']:
            results_list.append(item['screen_name'])
        print('Результаты поиска ids==>', results_list)
        return results_list

    def get_chosen_user_info(self, owner_id): #, count: int(10)): пока подставляю свой ID.
        params = get_params()
        params['user_ids'] = owner_id
        # params['count'] = count  # кол-во записей в выводе (умолч. - 1000)
        params['fields'] = 'sex, bdate, city, relation, verified, nickname, occupation,' \
                           'home_town, interests, books, contacts, about, activities' \
                           'has_photo, common_count, is_friend, personal, has_photo, photo_id,'

        URL = 'https://api.vk.com/method/users.get'
        response = requests.get(URL, params)
        # results_list = []
        pprint(response.text)
        # for item in response.json()['response']:
        #     print(item.items())
        #     results_list.append(item['id'])
        # return print('Результаты поиска ids==>', results_list)

class User:
    def __init__(self, token, owner_id: int):
        self.token = token
        self.owner_id = int(owner_id) # ID юзера в ВК



# CommonMethods.user_search(token,'Андрей Яковцев') #id344493552
CommonMethods.get_chosen_user_info(token, 'ayakovtsev')