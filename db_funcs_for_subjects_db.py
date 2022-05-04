import sqlite3


def create_db(db_name):

    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {db_name} (date text, time text)")


def create_db_imist(db_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE {db_name} (date text, time text, group_name text, subject text, subject_type text, location text, teacher text)")

def create_db_mag_fk(db_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE {db_name} (date text, time text, group_name text, subject text, subject_type text, location text, teacher text)")


def drop_db(db_name):

    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.executescript("DROP TABLE IF EXISTS " + db_name)


def check_is_null_in_db():
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    db_names = ['lovs_1', 'lovs_2', 'lovs_3', 'lovs_4',
                'zovs_1', 'zovs_2', 'zovs_3', 'zovs_4']
    for db_name in db_names:
        columns_names_in_db = f"PRAGMA table_info({db_name})"
        cursor.execute(columns_names_in_db)
        columns_names = cursor.fetchall()
        for column_name in columns_names:
            req = f"SELECT * FROM {db_name} WHERE {column_name[1]} IS NULL"
            cursor.execute(req)
            db_response = cursor.fetchall()
            if bool(db_response) is not False:
                message = f'null in {db_name} in {column_name}'
                return message
    return 'OK'


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
    cursor.execute(
        f"INSERT INTO {db_name} (date, time) VALUES ('{date}', '{time}')")
    conn.commit()


def save_date_and_time_and_group_imist(db_name, date, time, group_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO {db_name} (date, time, group_name) VALUES ('{date}', '{time}', '{group_name}')")
    conn.commit()

def save_date_and_time_and_group_mag_fk(db_name, date, time, group_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO {db_name} (date, time, group_name) VALUES ('{date}', '{time}', '{group_name}')")
    conn.commit()


def save_subj_imist(db_name, date, time, group, subj, subject_type, location, teacher):
    db_name = db_name
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    req = f"UPDATE {db_name} SET subject = '{subj}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET subject_type = '{subject_type}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET location = '{location}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET teacher = '{teacher}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

def save_subj_mag_fk(db_name, date, time, group, subj, subject_type, location, teacher):
    db_name = db_name
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    req = f"UPDATE {db_name} SET subject = '{subj}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET subject_type = '{subject_type}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET location = '{location}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()

    req = f"UPDATE {db_name} SET teacher = '{teacher}' WHERE date = '{date}' AND time = '{time}' AND group_name = '{group}'"
    cursor.execute(req)
    conn.commit()


def save_dates_and_times(db_name, list_of_dates, list_of_times):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    for list_dates in list_of_dates:
        for date in list_dates:
            for time in list_of_times:
                cursor.execute(
                    f"INSERT INTO {db_name} (date, time) VALUES ('{date}', '{time}')")
    conn.commit()


def save_subj(db_name, date, time, group, subj):
    db_name = db_name
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    req = f"UPDATE {db_name} SET {group} = '{subj}' WHERE date = '{date}' AND time = '{time}'"
    cursor.execute(req)
    conn.commit()


def is_group_exist(name_of_group, db_name):

    if name_of_group == 'группа_405' or name_of_group == 'группа_412' or name_of_group == 'группа_413':
        return True

    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    columns_names_in_db = f"PRAGMA table_info({db_name})"
    cursor.execute(columns_names_in_db)

    columns_names = [column_name[1] for column_name in cursor.fetchall()]
    for column_name in columns_names:
        if name_of_group in column_name:
            return True
    if name_of_group in columns_names:
        return True
    else:
        return False


def return_new_group_name(name_of_group, db_name):

    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    columns_names_in_db = f"PRAGMA table_info({db_name})"
    cursor.execute(columns_names_in_db)

    columns_names = [column_name[1] for column_name in cursor.fetchall()]
    for column_name in columns_names:
        if name_of_group in column_name:
            return column_name


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


def get_dates(db_name):
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()
    req = f"SELECT date FROM {db_name}"
    cursor.execute(req)
    return cursor.fetchall()


def get_db_name(name_of_group):
    #name_of_group = 'группа_' + str(name_of_group)

    con = sqlite3.connect('subjects.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_db_names = [db_name[0] for db_name in cursor.fetchall()]
    for db_name in all_db_names:
        cursor_for_name = con.cursor()
        columns_names_in_db = f"PRAGMA table_info({str(db_name)})"
        cursor_for_name.execute(columns_names_in_db)

        column_names = [column_name[1]
                        for column_name in cursor_for_name.fetchall()]
        for column_name in column_names:
            if name_of_group in column_name:
                return db_name
        if name_of_group in column_names:
            # TODO возможно убрать
            # костыль к изменению, где учебный отдел нашёл вторую 414 группу в университете
            if name_of_group == 'группа_414' and db_name == 'lovs_4_kurs':
                return 'zovs_4_kurs'
            elif name_of_group == 'группа_411' and db_name == 'lovs_4_kurs':
                return 'zovs_4_kurs'
            elif name_of_group == 'группа_412' and db_name == 'lovs_4_kurs':
                return 'zovs_4_kurs'
            elif name_of_group == 'группа_413' and db_name == 'lovs_4_kurs':
                return 'zovs_4_kurs'
            return db_name
    return None
