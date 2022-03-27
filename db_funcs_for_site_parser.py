import sqlite3


def create_db():
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE all_links (course_and_faculty text, link text, time_of_change text)')
    cursor.execute(
        'CREATE TABLE current_links (course_and_faculty text, link text)')


def drop_db():
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS all_links")
    cursor.executescript("DROP TABLE IF EXISTS current_links")


def drop_and_create_current_links_db():
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS current_links")
    cursor.executescript("DROP TABLE IF EXISTS all_links")
    cursor.execute(
        'CREATE TABLE all_links (course_and_faculty text, link text, time_of_change text)')
    cursor.execute(
        'CREATE TABLE current_links (course_and_faculty text, link text)')
    insert_link_to_current_links()


def insert_link_to_all_links(course_and_faculty, link, time_of_change):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO all_links(course_and_faculty, link, time_of_change) VALUES (?, ?, ?)',
                   (course_and_faculty, link, time_of_change))
    conn.commit()


def insert_link_to_current_links():
    group_names = [
        'lovs_1',
        'lovs_2',
        'lovs_3',
        'lovs_4',
        'zovs_1',
        'zovs_2',
        'zovs_3',
        'zovs_4',
        'imst_1_kurs',
        'imst_2_kurs',
        'imst_3_kurs',
        'imst_3_kurs',
        'magistracy_fk_full_time_1_kurs',
        'magistracy_fk_full_time_2_kurs',
        'magistracy_afk_full_time_1_kurs',
        'magistracy_afk_full_time_2_kurs',
        'magistracy_imst_full_time_1_kurs',
        'magistracy_imst_full_time_2_kurs',
    ]

    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    for name in group_names:
        cursor.execute(
            f"INSERT INTO current_links(course_and_faculty) VALUES ('{name}');")
        conn.commit()


def change_link_in_current_links(course_and_faculty, link):
    print('changed ' + link)
    correct_courese_and_faculty = get_correct_column_name(course_and_faculty)
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE current_links SET link = '{link}' WHERE course_and_faculty = '{correct_courese_and_faculty}'")
    conn.commit()

def get_correct_column_name(course_and_faculty):
    course_names = ['1_lovs', '1_zovs', '2_lovs', '2_zovs',
                        '3_lovs', '3_zovs', '4_lovs', '4_zovs']
    for name in course_names:
        if name in course_and_faculty:
            month = course_and_faculty[2:]
            day = course_and_faculty[0]
            correct_name = month + '_' + day
            return correct_name
        

def get_current_link(name):
    conn = sqlite3.connect('links_from_site.db')
    cursor = conn.cursor()

    req1 = "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'current_links'"
    cursor.execute(req1)

    if bool(cursor.fetchall()) == False:
        create_db()

    req = f"SELECT link FROM current_links WHERE course_and_faculty = '{name}'"
    cursor.execute(req)
    data = cursor.fetchall()
    if data == []:
        return False
    else:
        return data[0][0]


if __name__ == '__main__':
    drop_and_create_current_links_db()
