import sqlite3

def create_db(db_name):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {db_name} (date text, time text)")

def drop_db(db_name):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS " + db_name)
    
def save_groups(db_name, list_of_groups):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    for group in list_of_groups:
        cursor.execute(f"ALTER TABLE {db_name} ADD COLUMN {group} text")

def save_group(db_name, group_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE {db_name} ADD COLUMN {group_name} text")

def save_date_and_time(db_name, date, time):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {db_name} (date, time) VALUES ('{date}', '{time}')")
    conn.commit()

def save_dates_and_times(db_name, list_of_dates, list_of_times):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    
    for list_dates in list_of_dates:
        for date in list_dates:
            for time in list_of_times:
                cursor.execute(f"INSERT INTO {db_name} (date, time) VALUES ('{date}', '{time}')")
    conn.commit()

def save_subj(db_name, date, time, group, subj):
    db_name = db_name
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    
    req = f"UPDATE {db_name} SET {group} = '{subj}' WHERE date = '{date}' AND time = '{time}'"
    cursor.execute(req)
    conn.commit()

def get_subject_now(num_of_group, date, time):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

def get_subject_week(num_of_group, date):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

def is_group_exist(name_of_group, db_name):

    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    columns_names_in_db = f"PRAGMA table_info({db_name})"
    cursor.execute(columns_names_in_db)
    
    columns_names = [column_name[1] for column_name in cursor.fetchall()]
    if name_of_group in columns_names:
        return True
    else:
        return False

def get_subjects_today(name_of_group, db_name, date):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    
    day = str(date.day)
    if len(day) == 1:
        # нужно для базы данных, в которой формат дат состоит из двух чисел
        day = '0' + day
    month = str(date.month)
    if len(month) == 1:
        # нужно для базы данных, в которой формат дат состоит из двух чисел
        month = '0' + month
    current_date = day + '.' + month + '.'

    req = f"SELECT {name_of_group} FROM {db_name} WHERE date = '{current_date}'"
    cursor.execute(req)
    return cursor.fetchall()

def get_db_name(name_of_group):
    #name_of_group = 'Группа_' + str(name_of_group)

    con = sqlite3.connect('subjects.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_db_names = [db_name[0] for db_name in cursor.fetchall()]
    for db_name in all_db_names:
        cursor_for_name = con.cursor()
        columns_names_in_db = f"PRAGMA table_info({str(db_name)})"
        cursor_for_name.execute(columns_names_in_db)
        
        column_name = [column_name[1] for column_name in cursor_for_name.fetchall()]
        if name_of_group in column_name:
            #костыль к изменению, где учебный отдел нашёл вторую 414 группу в университете
            if name_of_group == 'группа_414' and db_name == 'lovs_4_kurs':
                continue 
            return db_name
    return None   
