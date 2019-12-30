import sqlite3

def create_db(db_name):
    
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS " + db_name)
    cursor.execute("CREATE TABLE " + db_name + " (date text, time text)")

def save_groups(db_name, list_of_groups):
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()

    for group in list_of_groups:   
        cursor.execute("ALTER TABLE " + db_name + " ADD COLUMN " + str(group) + " text")

def save_dates_and_times(db_name, list_of_dates, list_of_times):
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()
    
    for list_dates in list_of_dates:
        for date in list_dates:
            for time in list_of_times:
                cursor.execute("INSERT INTO " + db_name + " (date, time) VALUES ('" + date + "', '" + time + "')")
    conn.commit()

def save_subj(db_name, date, time, group, subj):
    db_name = db_name
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()
    
    string_sql = "UPDATE " + db_name + " SET " + group + " = '" + str(subj) + "' WHERE date = '" + str(date) + "' AND time = '" + str(time) + "'"
    
    cursor.execute(string_sql)
    conn.commit()

def get_subject_now(num_of_group, date, time):
    
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()


def get_subject_week(num_of_group, date):
    
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()


def get_subjects_today(name_of_group, db_name, date):
    
    conn = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = conn.cursor()
    columns_names_in_db = "PRAGMA table_info(" + str(db_name) + ")"
    cursor.execute(columns_names_in_db)
    
    columns_names = [column_name[1] for column_name in cursor.fetchall()]
    
    if name_of_group in columns_names:
        req = "SELECT " + str(name_of_group) + " FROM " + str(db_name) + " WHERE date = '" + str(date) + "'"
        cursor.execute(req)
        return cursor.fetchall()
    else:
        return False

def get_db_name(number_of_group):
    number_of_group = 'Группа_' + str(number_of_group)

    con = sqlite3.connect('subjects_PT_undergrade.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_db_names = [db_name[0] for db_name in cursor.fetchall()]
    for db_name in all_db_names:
        cursor_for_name = con.cursor()
        columns_names_in_db = "PRAGMA table_info(" + str(db_name) + ")"
        cursor_for_name.execute(columns_names_in_db)
        
        column_name = [column_name[1] for column_name in cursor_for_name.fetchall()]
        if number_of_group in column_name:
            return db_name
    return None   
