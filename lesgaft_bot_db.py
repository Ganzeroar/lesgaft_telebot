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

def get_group_number(user_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    req = "SELECT number_of_group FROM users WHERE chat_id = '" + str(user_id) + "'"

    cursor.execute(req)
    return cursor.fetchall()

def user_already_in_db(user_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    req = "SELECT chat_id FROM users"
    cursor.execute(req)
    users_list = [user_info[0] for user_info in cursor.fetchall()]

    if user_id in users_list:
        return True
    else:
        return False

def update_group(user_id, group_number):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    string_sql = "UPDATE users SET number_of_group  = " + str(group_number) + " WHERE chat_id = " + str(user_id)
    cursor.execute(string_sql)
    conn.commit()