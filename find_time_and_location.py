# -*- coding: utf-8 -*-

import pytz
import datetime
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import texts_for_lesgaft_bot
import find_class_location


def return_location_of_class(chat_id, text):
    name_of_location = text[3:].strip()
    if len(name_of_location) <= 3:
        try:
            int(name_of_location)
        except:
            return texts_for_lesgaft_bot.invalid_text
        print('User: ' + str(chat_id) +
              ' ask about location ' + str(name_of_location))
        location = find_class_location.find_class_location_used_number(
            name_of_location)
        return location
    elif 'кафедра' in name_of_location:
        location = find_class_location.find_department_location(
            name_of_location)
        return location
    elif 'факультет' in name_of_location:
        location = find_class_location.find_faculty_location(name_of_location)
        return location
    else:
        return 'Такой аудитории я не знаю'


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

    if check_time:
        check_time = check_time
    else:
        check_time = datetime.datetime.now(tz=msc_timezone).time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def return_text_about_time_before_lesson_with_location(chat_id, number_of_lesson, date, before_or_during='before'):
    number_of_group = db_funcs_for_students_db.get_group_number(chat_id)
    if number_of_group == False:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'группа_' + str(number_of_group)
    if name_of_group == 'группа_405' or name_of_group == 'группа_412' or name_of_group == 'группа_413' or name_of_group == 'группа_327' or name_of_group == 'группа_328':
        db_name = db_funcs_for_students_db.get_db_name(chat_id)
    else:
        db_name = db_funcs_for_subjects_db.get_db_name(name_of_group)
    if db_name == None:
        return 'Такой группы не существует. Измени номер группы.'

    if name_of_group == 'группа_327':
        name_of_group = db_funcs_for_students_db.return_new_group_name_327(chat_id)
    else:
        name_of_group = db_funcs_for_subjects_db.return_new_group_name(
            name_of_group, db_name)
            
    today_subjects = db_funcs_for_subjects_db.get_subjects_today(
        name_of_group, db_name, date)
    if len(today_subjects) == 5:
        if number_of_lesson == 5:
            return 'Сегодня у тебя больше нет пар'
    elif (len(today_subjects)) == 6:
        if number_of_lesson == 6:
            return 'Сегодня у тебя больше нет пар'
    if bool(today_subjects) == False or today_subjects == None:
        return texts_for_lesgaft_bot.error
    list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
    try:
        if today_subjects[number_of_lesson][0] != 'нет предмета':
            if before_or_during == 'before':
                next_subject = today_subjects[number_of_lesson][0]
                formate_of_time = '%H:%M'
                today_time = date.strftime("%H:%M")
                today_date = datetime.datetime.strptime(
                    today_time, formate_of_time)
                next_start_time = datetime.datetime.strptime(
                    list_of_times[number_of_lesson], formate_of_time)
                time_to_lesson = str(next_start_time - today_date)[0:4]
                class_location = find_class_location.find_class_location(
                    next_subject)
                text = f'Через {time_to_lesson} начнётся\n{next_subject}\n\n{class_location}'
                return text
            elif before_or_during == 'during':
                current_subject = today_subjects[number_of_lesson][0]
                class_location = find_class_location.find_class_location(
                    current_subject)
                text = f'Сейчас у вас {current_subject}\n\n{class_location}'
                return text
        if today_subjects[number_of_lesson][0] == 'нет предмета':
            return return_text_about_time_before_lesson_with_location(chat_id, number_of_lesson + 1, date)
        else:
            return []
    except Exception as exception:
        print('error ' + str(exception))


def return_time_before_class_and_location(chat_id):

    msc_timezone = pytz.timezone('Europe/Moscow')
    date = datetime.datetime.now(tz=msc_timezone)
    day_of_week = return_russian_day_of_week(str(date.strftime('%a')))

    if day_of_week == 'воскресенье':
        return 'Сегодня воскресенье, не учимся!'

    text = False

    if is_time_between(datetime.time(00, 00), datetime.time(9, 45)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 0, date)
    elif is_time_between(datetime.time(9, 45), datetime.time(11, 15)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 0, date, 'during')
    elif is_time_between(datetime.time(11, 15), datetime.time(11, 30)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 1, date)
    elif is_time_between(datetime.time(11, 30), datetime.time(13, 00)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 1, date, 'during')
    elif is_time_between(datetime.time(13, 00), datetime.time(13, 30)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 2, date)
    elif is_time_between(datetime.time(13, 30), datetime.time(15, 00)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 2, date, 'during')
    elif is_time_between(datetime.time(15, 00), datetime.time(15, 15)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 3, date)
    elif is_time_between(datetime.time(15, 15), datetime.time(16, 45)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 3, date, 'during')
    elif is_time_between(datetime.time(16, 45), datetime.time(17, 00)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 4, date)
    elif is_time_between(datetime.time(17, 00), datetime.time(18, 30)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 4, date, 'during')
    elif is_time_between(datetime.time(18, 30), datetime.time(18, 40)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 5, date)
    elif is_time_between(datetime.time(18, 40), datetime.time(21, 10)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 6, date, 'during')
    elif is_time_between(datetime.time(21, 10), datetime.time(00, 00)):
        text = return_text_about_time_before_lesson_with_location(
            chat_id, 6, date, 'during')
    print('User: ' + str(chat_id) + ' ask about where the lesson')

    if text == False:
        print(date)

    return text
