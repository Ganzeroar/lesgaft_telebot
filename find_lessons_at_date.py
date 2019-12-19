# -*- coding: utf-8 -*-

import pytz
import datetime
import find_time_and_location
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import texts_for_lesgaft_bot

def return_lessons_at_date(user_id, date):
    
    day_of_week = find_time_and_location.return_russian_day_of_week(str(date.strftime('%a')))
    if day_of_week == 'воскресенье':
        print('User: ' + str(user_id) +  ' from ask about tomorrow sunday')
        return 'Завтра воскресенье, не учимся!'
    number_of_group = db_funcs_for_students_db.get_group_number(user_id)
    if number_of_group == False:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = db_funcs_for_subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'

    day = str(date.day)
    if len(day) == 1:
        # нужно для базы данных, в которой формат дат состоит из двух чисел
        day = '0' + day
    current_date = day + '.' + str(date.month) + '.'
    subjects = db_funcs_for_subjects_db.get_subjects_today(name_of_group, db_name, current_date)
    if bool(subjects) == False:
        return 'Твоей группы не существует. Измени номер группы.'
    
    message_text = ''
    list_of_times = ['9:45-11:15 \n', '11:30-13:00 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
    number_of_date = date.strftime("%d.%m.%Y.")
    message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
    try:
        for x in range(5):
            message_text += list_of_times[x] + subjects[x][0] + '\n\n'
        print('User: ' + str(user_id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
        return message_text
    except Exception as exception:
        return texts_for_lesgaft_bot.error
