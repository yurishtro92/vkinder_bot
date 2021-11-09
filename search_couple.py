import requests
import operator


def get_couples(hometown, sex, relation, birth_year, token_app):  # подбор пары по введенным пользователем значениям
    url = 'https://api.vk.com/method/users.search'
    params = {
        'access_token': token_app,
        'count': '1000',
        'fields': ['sex', 'bdate', 'relation'],
        'hometown': hometown,
        'sex': sex,
        'relation': relation,
        'birth_year': birth_year,
        'v': '5.131',
    }
    res = requests.get(url, params=params)
    data = res.json()
    return data


def get_and_range_photos(id, token_app):  # получение 3-х самых популярных фото
    url1 = 'https://api.vk.com/method/photos.get'
    params1 = {
        'access_token': token_app,
        'album_id': 'profile',
        'owner_id': id,
        'extended': '1',
        'v': '5.131',
    }
    result = requests.get(url1, params=params1)
    photos = result.json()
    if list(photos.keys())[0] == 'error':  # обработка кейса при закрытом профиле найденной пары
        msg_string = 'Профиль закрыт настройками приватности, фото недоступны'
        return msg_string
    else:
        ranged_photos = {}
        for photo in photos['response']['items']:
            (photo['sizes']).reverse()
            ranged_photos[photo['sizes'][0]['url']] = photo['likes']['count'] + photo['comments']['count']  # словарь в
            # котором ключ - url фото в максимальном разрешении, значение - лайки+комментарии
        sorted_tuples = sorted(ranged_photos.items(), key=operator.itemgetter(1))
        sorted_ranged_photos = {k: v for k, v in sorted_tuples}  # сортировка словаря, чтобы получить 3 самых популярных фото
        if len(sorted_ranged_photos) >= 3:
            msg_string = list(sorted_ranged_photos.keys())[-1] + '\n' + list(sorted_ranged_photos.keys())[-2] + \
                         '\n' + list(sorted_ranged_photos.keys())[-3]
        elif len(sorted_ranged_photos) == 2:
            msg_string = list(sorted_ranged_photos.keys())[-1] + '\n' + list(sorted_ranged_photos.keys())[-2]
        elif len(sorted_ranged_photos) == 1:
            msg_string = list(sorted_ranged_photos.keys())[-1]
        else:
            msg_string = 'Фото профиля отсутствуют'
        return msg_string
