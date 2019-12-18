# -*- coding: utf-8 -*-

import pytz
import datetime
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import texts_for_lesgaft_bot
import find_class_location


def return_location_of_class(user_id, text):
    number_of_class = text[3:].strip()
    if len(number_of_class) > 3:
        return 'Такой аудитории я не знаю'
    try:
        int(number_of_class)
    except:
        return texts_for_lesgaft_bot.invalid_text
    print('User: ' + str(user_id) + ' ask about location ' + str(number_of_class))
    return find_class_location.find_class_location_used_number(number_of_class)


def return_russian_day_of_week(eng_day):
    if eng_day == 'Mon':
        return 'понедельник'
    elif eng_day == 'Tue':
        return 'вторник'
    elif eng_day == 'Wed':
        return 'среду'
    elif eng_day == 'Thu':
        return 'четверг'
    elif eng_day == 'Fri':
        return 'пятницу'
    elif eng_day == 'Sat':
        return 'субботу'
    elif eng_day == 'Sun':
        return 'воскресенье'

def is_time_between(begin_time, end_time, check_time=None):
    msc_timezone = pytz.timezone('Europe/Moscow')

    check_time = check_time or datetime.datetime.now(tz=msc_timezone).time()
    #check_time = datetime.time(10,10)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def return_message_text_about_current_lesson(user_id, number_of_lesson):
    msc_timezone = pytz.timezone('Europe/Moscow')
    
    number_of_group = db_funcs_for_students_db.get_group_number(user_id)
    if number_of_group == False:    
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = db_funcs_for_subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    
    date_and_time_now = datetime.datetime.now(tz=msc_timezone)
    day = str(date_and_time_now.day)
    if len(day) == 1:
        day = '0' + day
    today_date = day + '.' + str(date_and_time_now.month) + '.'
    today_subjects = db_funcs_for_subjects_db.get_subjects_today(name_of_group, db_name, today_date)
    if bool(today_subjects) == False or today_subjects[number_of_lesson][0] == None:
        return texts_for_lesgaft_bot.error
    else:
        list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
    try:
        if today_subjects[number_of_lesson][0] != 'Нет предмета':
            current_subject = today_subjects[number_of_lesson][0]
            class_location = find_class_location.find_class_location(current_subject)
            text = f'Сейчас у вас {current_subject}\n\n{class_location}'
            return text
        if today_subjects[number_of_lesson][0] == 'Нет предмета':
            return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        else:
            return [[]]
    except Exception as exception:
        print('error ' + str(exception))
    
def return_message_text_to_about_time_before_lesson(user_id, number_of_lesson):
    msc_timezone = pytz.timezone('Europe/Moscow')

    number_of_group = db_funcs_for_students_db.get_group_number(user_id)
    if number_of_group == False:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = db_funcs_for_subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    
    date_and_time_now = datetime.datetime.now(tz=msc_timezone)
    day = str(date_and_time_now.day)
    if len(day) == 1:
        day = '0' + day
    today_date = day + '.' + str(date_and_time_now.month) + '.'
    today_subjects = db_funcs_for_subjects_db.get_subjects_today(name_of_group, db_name, today_date)
    if number_of_lesson >= 5:
        return 'Сегодня у тебя больше нет пар.' 
    if bool(today_subjects) == False or today_subjects[number_of_lesson][0] == None:
        return texts_for_lesgaft_bot.error
    else:
        list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
    try:
        if today_subjects[number_of_lesson][0] != 'Нет предмета':
            next_subject = today_subjects[number_of_lesson][0]
            formate_of_time = '%H:%M' 
            today_time = date_and_time_now.strftime("%H:%M")
            today_date = datetime.datetime.strptime(today_time, formate_of_time)
            next_start_time = datetime.datetime.strptime(list_of_times[number_of_lesson], formate_of_time)
            time_to_lesson = str(next_start_time - today_date)[0:4]
            class_location = find_class_location.find_class_location(next_subject)
            text = f'Через {time_to_lesson} начнётся {next_subject}\n\n{class_location}' 
            return text
        if today_subjects[number_of_lesson][0] == 'Нет предмета':
            return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        else:
            return []
    except Exception as exception:
        print('error ' + str(exception))


def return_time_class_location(user_id):
    msc_timezone = pytz.timezone('Europe/Moscow')

    time_now = datetime.datetime.now(tz=msc_timezone)
    day_of_week = return_russian_day_of_week(str(time_now.strftime('%a')))
    if day_of_week == 'воскресенье':
        return 'Сегодня воскресенье, не учимся!'

    text = ''

    if is_time_between(datetime.time(00,00), datetime.time(9,44)):
        text = return_message_text_to_about_time_before_lesson(user_id, 0)
    elif is_time_between(datetime.time(9,45), datetime.time(11,15)):
        text = return_message_text_about_current_lesson(user_id, 0)
    elif is_time_between(datetime.time(11,16), datetime.time(11,29)):
        text = return_message_text_to_about_time_before_lesson(user_id, 1)
    elif is_time_between(datetime.time(11,30), datetime.time(13,00)):
        text = return_message_text_about_current_lesson(user_id, 1)
    elif is_time_between(datetime.time(13,1), datetime.time(13,29)):
        text = return_message_text_to_about_time_before_lesson(user_id, 2)
    elif is_time_between(datetime.time(13,30), datetime.time(15,00)):
        text = return_message_text_about_current_lesson(user_id, 2)
    elif is_time_between(datetime.time(15,1), datetime.time(15,14)):
        text = return_message_text_to_about_time_before_lesson(user_id, 3)
    elif is_time_between(datetime.time(15,15), datetime.time(16,45)):
        text = return_message_text_about_current_lesson(user_id, 3)
    elif is_time_between(datetime.time(16,46), datetime.time(16,59)):
        text = return_message_text_to_about_time_before_lesson(user_id, 4)
    elif is_time_between(datetime.time(17,00), datetime.time(18,30)):
        text = return_message_text_about_current_lesson(user_id, 4)
    elif is_time_between(datetime.time(18,31), datetime.time(23,59)):
        text = return_message_text_to_about_time_before_lesson(user_id, 5)
    print('User: ' + str(user_id) + ' ask about where the lesson')
    return text
