import requests

def token_check(token_id):
    URL = 'https://api.vk.com/method/users.get'
    params = {
        'access_token':  token_id,
        'user_id': '585749225',
        'fields': ['photo_50','verified'],
        'name_case': 'Nom',
        'v': '5.131',
    }
    res = requests.get(URL, params = params)
    data = res.json()
    for i in data:
        if i == 'response':
            flag = 1
        if i == 'error':
            flag = 2
    return flag



