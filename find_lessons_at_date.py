# -*- coding: utf-8 -*-

import pytz
import datetime
import find_time_and_location
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import texts_for_lesgaft_bot


def return_lessons_at_date(user_id, date):
    day_of_week = find_time_and_location.return_russian_day_of_week(
        str(date.strftime('%a')))
    if day_of_week == 'воскресенье':
        print('User: ' + str(user_id) + ' from ask about tomorrow sunday')
        return texts_for_lesgaft_bot.sunday_text
    number_of_group = db_funcs_for_students_db.get_group_number(user_id)
    if number_of_group == False:
        return texts_for_lesgaft_bot.user_not_in_db
    name_of_group = 'группа_' + str(number_of_group)
    if name_of_group == 'группа_405' or name_of_group == 'группа_412' or name_of_group == 'группа_413' or name_of_group == 'группа_327' or name_of_group == 'группа_328':
        db_name = db_funcs_for_students_db.get_db_name(user_id)
    else:
        db_name = db_funcs_for_subjects_db.get_db_name(name_of_group)
    if db_name == None or db_funcs_for_subjects_db.is_group_exist(name_of_group, db_name) == False:
        return texts_for_lesgaft_bot.group_is_not_exist

    if name_of_group == 'группа_327':
        name_of_group = db_funcs_for_students_db.return_new_group_name_327(user_id)
    else:
        name_of_group = db_funcs_for_subjects_db.return_new_group_name(
            name_of_group, db_name)

    subjects = db_funcs_for_subjects_db.get_subjects_today(
        name_of_group, db_name, date)
    if bool(subjects) == False:
        return texts_for_lesgaft_bot.error

    number_of_date = date.strftime("%d.%m.%Y.")
    if set(subjects) == {('нет предмета',)}:
        print('User: ' + str(user_id) + ' from ' +
              str(number_of_group) + ' ask about ' + str(number_of_date))
        return 'В ' + day_of_week + f' ({number_of_date}) у тебя нет пар' if day_of_week != 'вторник' else 'Во ' + day_of_week + f' ({number_of_date}) у тебя нет пар'
    message_text = ''
    list_of_times = ['9:45-11:15\n', '11:30-13:00\n', '13:30-15:00\n',
                     '15:15-16:45\n', '17:00-18:30\n', '18:40-20:10\n']
    message_text += f'Расписание на {day_of_week} ({number_of_date})\n\n'
    try:
        for x in range(len(subjects)):
            if subjects[x][0] != 'нет предмета':
                message_text += list_of_times[x] + subjects[x][0] + '\n\n'
        print('User: ' + str(user_id) + ' from ' +
              str(number_of_group) + ' ask about ' + str(number_of_date))
        return message_text
    except:
        return texts_for_lesgaft_bot.error
