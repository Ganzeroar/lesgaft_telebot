import sqlite3
import texts_for_lesgaft_bot
import os


def create_db(path = None):
    if path == None:
        conn = sqlite3.connect("students.db")
    else:
        current_path = os.path.dirname(os.path.abspath(__file__))
        new_path = os.path.join(current_path, f'{path}\students.db')
        conn = sqlite3.connect(new_path)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE users
                    (chat_id integer, first_name text, last_name text,
                    registration_date integer, number_of_group integer,
                    academic_degree text, education_form text, 
                    number_of_course integer, timetable_name text,
                    in_registration_process text, is_subscribe_to_newsletter integer)
                    """)


def add_columns_for_update():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute(
        f"ALTER TABLE users ADD COLUMN is_subscribe_to_newsletter integer")


def drop_db(path = None):
    if path == None:
        conn = sqlite3.connect("students.db")
    else:
        current_path = os.path.dirname(os.path.abspath(__file__))
        new_path = os.path.join(current_path, f'{path}\students.db')
        conn = sqlite3.connect(new_path)

    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS users")


def get_subscribe_in_newsletter_status(user_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT is_subscribe_to_newsletter FROM users WHERE chat_id = {user_id}"
    cursor.execute(string_sql)
    bool_state = bool(cursor.fetchall()[0][0])
    return bool_state


def get_subscribed_to_newsletter_users():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT chat_id FROM users WHERE is_subscribe_to_newsletter = 1"
    cursor.execute(string_sql)
    subscribed_users = cursor.fetchall()
    return subscribed_users


def set_is_subscribe_to_newsletter(chat_id, bool_value):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if bool_value == True:
        bool_value = 1
    elif bool_value == False:
        bool_value = 0

    string_sql = f"UPDATE users SET is_subscribe_to_newsletter = '{bool_value}' WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()


def set_in_registration_process(chat_id, bool_value):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    string_sql = f"UPDATE users SET in_registration_process = '{bool_value}' WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()


def get_state_of_registragion_process(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT in_registration_process FROM users WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    bool_state = bool(cursor.fetchall()[0][0])
    return bool_state


def save_timetable_name(chat_id, timetable_name, number_of_group):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    string_sql = f"UPDATE users SET timetable_name = '{timetable_name}' WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()
    string_sql = f"UPDATE users SET number_of_group  = {number_of_group} WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()
    text = texts_for_lesgaft_bot.create_message_group_was_recorded(number_of_group)
    return text

def get_db_name(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql =  f"SELECT timetable_name FROM users WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    db_name = cursor.fetchall()[0][0]
    return db_name



def save_number_of_course(chat_id, name_of_course):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    number_of_course = name_of_course[0]

    string_sql = f"UPDATE users SET number_of_course = {number_of_course} WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()


def get_number_of_course(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT number_of_course FROM users WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    number_of_course = cursor.fetchall()[0][0]
    return number_of_course


def save_education_form(chat_id, education_form):
    # используется только для 327 группы
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"UPDATE users SET education_form = '{education_form}' WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()

def return_new_group_name_327(user_id):
    group_name = get_education_form(user_id)
    return group_name

def get_education_form(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT education_form FROM users WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    return cursor.fetchall()[0][0]


def save_academic_degree(chat_id, academic_degree):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"UPDATE users SET academic_degree = '{academic_degree}' WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()


def get_academic_degree(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    string_sql = f"SELECT academic_degree FROM users WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    academic_degree = cursor.fetchall()[0][0]
    return academic_degree


def starting_insert_data(chat_id, first_name, last_name, date_of_registation):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users(chat_id, first_name, last_name, registration_date) VALUES (?, ?, ?, ?)",
                   (chat_id, first_name, last_name, date_of_registation))
    conn.commit()


def get_all_users():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    req = "SELECT chat_id FROM users;"
    cursor.execute(req)
    users = cursor.fetchall()
    return users


def get_group_number(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    req = f"SELECT number_of_group FROM users WHERE chat_id = {chat_id}"
    cursor.execute(req)
    data = cursor.fetchall()
    if data == []:
        return False
    else:
        return data[0][0]


def user_already_in_db(chat_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    req = "SELECT chat_id FROM users"
    cursor.execute(req)
    users_list = [user_info[0] for user_info in cursor.fetchall()]

    if chat_id in users_list:
        return True
    else:
        return False


def update_group(chat_id, number_of_group):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    string_sql = f"UPDATE users SET number_of_group  = {number_of_group} WHERE chat_id = {chat_id}"
    cursor.execute(string_sql)
    conn.commit()


def overwrite_group(message_text, chat_id):
    number_of_group = int(message_text)
    update_group(chat_id, number_of_group)
    text = texts_for_lesgaft_bot.create_message_group_was_recorded(number_of_group)
    print(f'User: {str(chat_id)} changed his group to {str(number_of_group)}')
    return text


if __name__ == "__main__":
    create_db()
