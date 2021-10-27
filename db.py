import psycopg2

def write_db(id, photos):
  connection = psycopg2.connect(#установка соединения с БД (в данном случае локальная БД)
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
  insert_query = f"INSERT INTO data (VK_ID, PHOTOS) VALUES ('{id}', '{photos}');"#запись в БД результата работы скрипта -
  # пары "ссылка на профиль" - "3 самых популярных фото"
  cur.execute(insert_query)
  connection.commit()
  connection.close()
