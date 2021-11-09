import psycopg2


def write_db(id, photos):
    # установка соединения с БД (в данном случае локальная БД)
    try:
        connection = psycopg2.connect(
          database="homework_1",
          user="user_1",
          password="user1",
          host="localhost",
          port="5432"
        )
        cur = connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS data
           (
           ID SERIAL PRIMARY KEY,
           VK_ID VARCHAR(64), 
           PHOTOS TEXT  
           );''')
        insert_query = f"INSERT INTO data (VK_ID, PHOTOS) VALUES ('{id}', '{photos}');"  # запись в БД результата работы
        # скрипта - пары "ссылка на профиль" - "3 самых популярных фото"
        cur.execute(insert_query)
        connection.commit()
        connection.close()
        flag_db = 1
        return flag_db
    except psycopg2.OperationalError:  # обработка кейса ошибки при подключении к базе данных
        flag_db = 0
        return flag_db
