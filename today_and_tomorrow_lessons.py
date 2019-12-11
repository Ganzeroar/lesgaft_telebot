# -*- coding: utf-8 -*-

import pytz
import datetime
import time_class_and_location
import only_students_db
import subjects_db
import texts_for_lesgaft_bot

def return_today_lessons(user_id):

    msc_timezone = pytz.timezone('Europe/Moscow')

    time_now = datetime.datetime.now(tz=msc_timezone)
    day_of_week = time_class_and_location.return_russian_day_of_week(str(time_now.strftime('%a')))
    if day_of_week == 'воскресенье':
        return 'Сегодня воскресенье, не учимся!'
    number_of_group = only_students_db.get_group_number(user_id)
    if number_of_group == False:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    
    day = str(time_now.day)
    if len(day) == 1:
        # нужно для базы данных, в которой формат дат состоит из двух чисел
        day = '0' + day
    today_date = day + '.' + str(time_now.month) + '.'
    
    today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
    if today_subjects == False:
        return 'Твоей группы не существует. Измени номер группы.'
    
    message_text = ''
    list_of_times = ['9:45-11:15 \n', '11:30-13:30 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
    number_of_date = time_now.strftime("%d.%m.%Y.")
    message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
    try:
        for x in range(5):
            message_text += list_of_times[x] + today_subjects[x][0] + '\n\n'
        print('User: ' + str(user_id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
        return message_text
    except Exception as exception:
        return texts_for_lesgaft_bot.error

def return_tomorrow_lessons(user_id):

    msc_timezone = pytz.timezone('Europe/Moscow')
    
    time_now = datetime.datetime.now(tz=msc_timezone)
    tomorrow = time_now + datetime.timedelta(days=1)
    day_of_week = time_class_and_location.return_russian_day_of_week(str(tomorrow.strftime('%a')))
    if day_of_week == 'воскресенье':
        return 'Завтра воскресенье, не учимся!'
    number_of_group = only_students_db.get_group_number(user_id)
    if number_of_group == False:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'

    day = str(time_now.day + 1)
    if len(day) == 1:
        # нужно для базы данных, в которой формат дат состоит из двух чисел
        day = '0' + day
    tomorrow_date = day + '.' + str(time_now.month) + '.'
    tomorrow_subjects = subjects_db.get_subjects_today(name_of_group, db_name, tomorrow_date)
    if tomorrow_subjects == False:
        return 'Твоей группы не существует. Измени номер группы.'
    
    message_text = ''
    list_of_times = ['9:45-11:15 \n', '11:30-13:00 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
    number_of_date = tomorrow.strftime("%d.%m.%Y.")
    message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
    try:
        for x in range(5):
            message_text += list_of_times[x] + tomorrow_subjects[x][0] + '\n\n'
        print('User: ' + str(user_id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
        return message_text
    except Exception as exception:
        print(exception)
        return texts_for_lesgaft_bot.error
