# -*- coding: utf-8 -*-

import lesgaft_bot_db
import subjects_db
import datetime
import time
import pytz
import texts_for_lesgaft_bot

def return_russian_day_of_week(eng_day):
    if eng_day == 'Mon':
        return 'понедельник'
    elif eng_day == 'Tue':
        return 'вторник'
    elif eng_day == 'Wed':
        return 'среду'
    elif eng_day == 'Thu':
        return 'четеверг'
    elif eng_day == 'Fri':
        return 'пятницу'
    elif eng_day == 'Sat':
        return 'субботу'
    elif eng_day == 'Sun':
        return 'воскресенье'
    
def return_message_text_about_current_lesson(user_id, number_of_lesson):

    msc_timezone = pytz.timezone('Europe/Moscow')

    try:
        number_of_group = lesgaft_bot_db.get_group_number(user_id)[0][0]
    except:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    else:
        #d = datetime.date(2019, 11, 18)
        #t = datetime.time(10, 10)
        #date_and_time_now =  datetime.datetime.combine(d, t)
        date_and_time_now = datetime.datetime.now(tz=msc_timezone)
        today_date = str(date_and_time_now.day) + '.' + str(date_and_time_now.month) + '.'
        today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
        if bool(today_subjects) == False or today_subjects[number_of_lesson][0] == None:
            return texts_for_lesgaft_bot.error
        else:
            list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
        try:
            if today_subjects[number_of_lesson][0] != 'Нет предмета':
                current_subject = today_subjects[number_of_lesson][0]
                text = f'Сейчас у вас {current_subject}'
                return text
            if today_subjects[number_of_lesson][0] == 'Нет предмета':
                return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        except Exception as exception:
            print('error ' + str(exception))
    
def return_message_text_to_about_time_before_lesson(user_id, number_of_lesson):
    msc_timezone = pytz.timezone('Europe/Moscow')

    try:
        number_of_group = lesgaft_bot_db.get_group_number(user_id)[0][0]
    except:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    else:
        #d = datetime.date(2019, 11, 21)
        #t = datetime.time(6, 0)
        #date_and_time_now =  datetime.datetime.combine(d, t)
        date_and_time_now = datetime.datetime.now(tz=msc_timezone)
        today_date = str(date_and_time_now.day) + '.' + str(date_and_time_now.month) + '.'
        today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
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
                text = f'Через {time_to_lesson} начнётся {next_subject}'
                return text
            if today_subjects[number_of_lesson][0] == 'Нет предмета':
                return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        except Exception as exception:
            print('error ' + str(exception))
            