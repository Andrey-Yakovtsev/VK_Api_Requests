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

class User:
    def __init__(self, token):
        self.token = token

    def get_chosen_user_info(self): #пока подставляю случайны ID - 1й в индерсе поиска.
        matched_user = User.relation_ready_user_search(token, 'Андрей Яковцев')
        params = get_params()
        params['user_ids'] = matched_user[0] #ID - 1й в индексе поиска.
        # params['count'] = count  # кол-во записей в выводе (умолч. - 1000)
        params['fields'] = 'sex, bdate, city, relation, verified, nickname, occupation,' \
                           'home_town, interests, books, contacts, about, activities' \
                           'has_photo, common_count, is_friend, personal, has_photo, photo_max,'

        URL = 'https://api.vk.com/method/users.get'
        response = requests.get(URL, params)
        # pprint(response.json()['response'][0])
        return response.json()['response'][0]


    def relation_ready_user_search(self, search_query: str):
        mega_search_result = []
        i=1
        for symbol in search_query:
            # print(symbol)
            params = get_params()
            params['q'] = symbol
            params['count'] = 10 #999
            params['has_photo'] = 1 # без фотки не выводятся
            params['fields'] = 'relation, sex, city, bdate, screen_name, photo_200' #добрать параметров
            URL = 'https://api.vk.com/method/users.search'
            response = requests.get(URL, params)
            time.sleep(0.4)
            print('Запрос:==>', i)
            i+=1
            proper_status = '0156' # Это статусы тех, кто открыто их объявил. Без указания статуса (None) исключены
            # print(response.text) # тут упоминается 241 млн записей: {"response":{"count":241720908,"items":...
            for user in response.json()['response']['items']:
                if str(user.get('relation')) in proper_status:
                    mega_search_result.append(user['id'])
        print('Подходящий статус у ids==>', len(mega_search_result), mega_search_result) #, results_list)
        return mega_search_result #можно впринципе пройтись разок поиском и все итоги убрать в базу

class Matching:
    '''
    функции проверки параметров соответствия юзеров из полученной базы нашему юзеру
    Получают на вход юзера, выдают рейтинги соответствия каждого юзера выбранному
    '''
    # matched_user = User.get_chosen_user_info(token)
    # user_sex = matched_user['sex']
    # user_bdate = matched_user['bdate'].split('.')
    # city = matched_user['city']['title']

    def matching_sex(self):
        # for user in response.json()['response']['items']:
        #     if user['sex'] != user_sex: #выборка оп полу
        pass

    def mathcing_age_delta(self):
        pass

    def matching_location(self):
        if str(user.get('city')) == city and not None:
                    print(user.get('city'))
        pass
# User.get_chosen_user_info(token).relation_ready_user_search(token,'Андрей Яковцев') #id344493552
# User.get_chosen_user_info(token)
User.relation_ready_user_search(token, 'абв')