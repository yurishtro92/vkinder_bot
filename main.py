from random import randrange
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
from search_couple import get_couples, get_and_range_photos
from db import write_db

with open('token_bot.txt', 'r') as file:
    token_bot = file.read().strip()
with open('token_app.txt', 'r') as file:
    token_app = file.read().strip()
vk = vk_api.VkApi(token=token_bot)
longpoll = VkLongPoll(vk)


class VKinder:

    def write_msg(self, message):
        vk.method('messages.send', {'user_id': self, 'message': message, 'random_id': randrange(10 ** 7), })
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                user_id = event.raw[3]
                if request == "/start":
                    write_msg(event.user_id, "Для начала поиска пары введите команду /search_couple")
                    break
                else:
                    write_msg(event.user_id, "Некорректная команда")

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
                if len(request) != 4:
                    write_msg(event.user_id, "Некорректный ввод данных. Введите недостающие данные")
                else:
                    search_result = {}# в этом словаре ведется учет пар, выданных при первом
                    # поиске, чтобы не выдавать их при повторном поиске
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
                    get_couples(hometown, sex, relation, birth_year, token_app)
                    for person in get_couples(hometown, sex, relation, birth_year, token_app)['response']['items']:
                        if str(dict(person)['id']) in search_result:  # пропуск ранее выданных id при повторном запросе,
                            # чтобы не повторять результат выдачи профилей
                            pass
                        else:
                            get_and_range_photos(str(dict(person)['id']), token_app)
                            # формирование сообщения в виде: ссылка на профиль и 3 самых популярных фото
                            write_msg(event.user_id, 'https://vk.com/id' + str(dict(person)['id']) + '\n'
                                      + get_and_range_photos(str(dict(person)['id']), token_app))
                            # запись результатов поиска пары в search_result
                            search_result['https://vk.com/id' + str(dict(person)['id'])] = get_and_range_photos(
                                str(dict(person)['id']), token_app)
                            # запись результатов поиска пары в БД
                            write_db('https://vk.com/id' + str(dict(person)['id']), get_and_range_photos(str(dict(person)['id']), token_app))
                    if write_db('https://vk.com/id' + str(dict(person)['id']), get_and_range_photos(str(dict(person)['id']), token_app)) == 1:
                        write_msg(event.user_id,
                                    "Поиск окончен. Результаты поиска записаны в базу данных")
                            # если БД по каким-либо причинам недоступна, результаты поиска выгружаются в json-файл
                    elif write_db('https://vk.com/id' + str(dict(person)['id']), get_and_range_photos(str(dict(person)['id']), token_app)) == 0:
                        with open('search_result.json', 'w+') as f:
                            json.dump(search_result, f)
                        write_msg(event.user_id,
                                      "Ошибка авторизации базы данных. Результаты поиска записаны в json файл")


if __name__ == '__main__':
    vkinder = VKinder()