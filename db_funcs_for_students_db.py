import sqlite3
import texts_for_lesgaft_bot

def create_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE users
                    (chat_id integer, first_name text, last_name text,
                    registration_date integer, number_of_group integer)
                    """)

def drop_db():
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS users")
    

def starting_insert_data(chat_id, first_name, last_name, date_of_registation):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users(chat_id, first_name, last_name, registration_date) VALUES (?, ?, ?, ?)", (chat_id, first_name, last_name, date_of_registation))
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

def update_group(chat_id, group_number):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    string_sql = f"UPDATE users SET number_of_group  = {str(group_number)} WHERE chat_id = {str(chat_id)}"
    cursor.execute(string_sql)
    conn.commit()

def overwrite_group(message_text, chat_id):
    number_of_group = int(message_text)
    update_group(chat_id, number_of_group)
    text = f'Ваша группа {number_of_group} записана!' + texts_for_lesgaft_bot.group_saved
    print('User: ' + str(chat_id) +  ' changed his group to ' + str(number_of_group))
    return text

if __name__ == "__main__":
    create_db()
