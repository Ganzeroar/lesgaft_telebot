import sqlite3

def create_db():
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE all_links (course_and_faculty text, link text, time_of_change text)')
    cursor.execute('CREATE TABLE current_links (course_and_faculty text, link text)')

def insert_link_to_all_links(course_and_faculty, link, time_of_change):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO all_links(course_and_faculty, link, time_of_change) VALUES (?, ?, ?)', (course_and_faculty, link, time_of_change))
    conn.commit()

def insert_link_to_current_links(course_and_faculty, link):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO current_links(course_and_faculty, link) VALUES (?, ?)', (course_and_faculty, link))
    conn.commit()


def change_link_in_current_links(course_and_faculty, link):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE current_links SET link = '{link}' WHERE course_and_faculty = '{course_and_faculty}'")
    conn.commit()

def get_current_links():
    # пока нигде не используется
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    cursor.execute('SELECT link FROM current_links')
    data = cursor.fetchall()
    return data

def get_current_link(course_and_faculty):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    req1 = "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'current_links'"
    cursor.execute(req1)

    if bool(cursor.fetchall()) == False:
        create_db()

    req = f"SELECT link FROM current_links WHERE course_and_faculty = '{course_and_faculty}'"
    cursor.execute(req)
    data = cursor.fetchall()
    if data == []:
        return False
    else:
        return data[0][0]

if __name__ == '__main__':
    create_db()
