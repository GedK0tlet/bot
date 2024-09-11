import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS DataS (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
theme TEXT NOT NULL,
many_money TEXT NOT NULL,
valute TEXT NOT NULL,
link TEXT NOT NULL,
date TEXT NOT NULL,
month TEXT NOT NULL
)
''')

connection.commit()
connection.close()

def wrote_in_db(username: str, theme: str, many_money: str, valute: str, link: str, date: str):
    month_m = ""
    with open("month.txt", "r") as month:
        month_m = month.readline()
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO DataS (username, theme, many_money, valute, link, date, month) VALUES (?, ?, ?, ?, ?, ?, ?)', (f'{username}', f'{theme}', f'{many_money}', f'{valute}', f'{link}', f'{date}', f'{month_m}'))

    connection.commit()
    connection.close()

def from_db_take(month: str):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM DataS WHERE month = "{month}"')
    data = cursor.fetchall()
    ar = []
    for item in data:
        my_dict = {
            "id":item[0],
            "username":item[1],
            "theme":item[2],
            "many_money":item[3],
            "valute":item[4],
            "path":item[5],
            "date":item[6],
            "month": item[7]
        }
        ar.append(my_dict)
    connection.close()
    return ar