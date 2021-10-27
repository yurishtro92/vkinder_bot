from random import randrange
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from search_couple import get_couples, get_and_range_photos
from db import write_db
from token_check import token_check

token_bot = 'токен сообщества вк'
vk = vk_api.VkApi(token=token_bot)
longpoll = VkLongPoll(vk)

class VKinder:
    def __init__(self, user_id):
        self.user_id = user_id

    def write_msg(self, message):
        vk.method('messages.send', {'user_id': self, 'message': message, 'random_id': randrange(10 ** 7), })
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "/start":
                    write_msg(event.user_id, "Введите token id")
                    break
                else:
                    write_msg(event.user_id, "Некорректная команда")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                token_id = request
                # обработка кейса ввода некорректного токена
                if token_check(request) == 1:
                     write_msg(event.user_id,
                              "Токен получен. Для начала поиска пары введите команду /search_couple")
                     break
                if token_check(request) == 2:
                     write_msg(event.user_id,
                               "Некорректный токен. Заново пройдите процедуру получения токена и введите его")
                else:
                    write_msg(event.user_id, "Некорректный токен. Заново пройдите процедуру получения токена и введите его")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "/search_couple":
                    write_msg(event.user_id, f"Введите данные для поиска в формате: пол(м или ж), год рождения, Город, "
                                             f"отношения(свободен(-дна), замужем(женат))")
                    break
                else:
                    write_msg(event.user_id, "Некорректная команда")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.split()
                if len(request) !=4:
                    write_msg(event.user_id, "Некорректный ввод данных. Введите недостающие данные")
                else:
                    id_list = []  # в этом списке ведется учет выданных при первом поиске id, чтобы потом не выдавать их при повторном поиске
                    if request[0] == 'ж':
                        sex = 1
                    elif request[0] == 'м':
                        sex = 2
                    birth_year = request[1]
                    hometown = request[2]
                    if request[3] == 'свободен' or 'свободна':
                        relation = 0
                    elif request[3] == 'женат' or 'замужем':
                        relation = 1
                    get_couples(hometown, sex, relation, birth_year, token_id)
                    for person in get_couples(hometown, sex, relation, birth_year, token_id)['response']['items']:
                        if str(dict(person)['id']) in id_list:#пропуск ранее выданных id при повторном запросе,
                            # чтобы не повторять результат выдачи
                            pass
                        else:
                            get_and_range_photos(str(dict(person)['id']), token_id)
                            #формирование сообщения в виде: ссылка на профиль и 3 самых популярных фото
                            write_msg(event.user_id, 'https://vk.com/id' + str(dict(person)['id']) + '\n'
                                      + get_and_range_photos(str(dict(person)['id']), token_id))
                            #запись результата в БД
                            write_db('https://vk.com/id' + str(dict(person)['id']), get_and_range_photos(str(dict(person)['id']), token_id))

if __name__ == '__main__':
    vkinder = VKinder(585749225)


