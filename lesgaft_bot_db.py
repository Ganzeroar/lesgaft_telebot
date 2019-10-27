import sqlite3


def create_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    
    # Создание таблицы
    cursor.execute("""CREATE TABLE users
                      (chat_id integer, first_name text, last_name text,
                      registarion_date integer, number_of_group integer)
                   """)

def starting_insert_data(student_info):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", student_info)
    conn.commit()
#create_db()