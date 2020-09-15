import telebot
import time
import logging
import datetime
import pytz

import db_funcs_for_students_db
import texts_for_lesgaft_bot
import find_time_and_location
import find_lessons_at_date
import handler_of_unusual_requests as handler

def change_group_old(user_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)

    text = db_funcs_for_students_db.overwrite_group(message_text, user_id)
    return text, main_keyboard

def return_where_is_the_lesson(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)
    text = find_time_and_location.return_time_before_class_and_location(chat_id)
    return text, main_keyboard

def return_today_lessons(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    text = find_lessons_at_date.return_lessons_at_date(chat_id, time_now)
    return text, main_keyboard

def return_tomorrow_lessons(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    tomorrow = time_now + datetime.timedelta(days=1)
    text = find_lessons_at_date.return_lessons_at_date(chat_id, tomorrow)
    return text, main_keyboard

def return_where_is_the_classroom(chat_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)

    text = find_time_and_location.return_location_of_class(chat_id, message_text)
    return text, main_keyboard



def main_request_handler(message_text, user_id):
    message_text = message_text.lower()

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    text, keyboard = '', ''
    if len(message_text) == 3 and message_text.isdigit():
        text, keyboard = change_group_old(user_id, message_text)
    elif message_text == 'где пара?':
        text, keyboard = return_where_is_the_lesson(user_id)
    elif message_text == 'какие сегодня пары?':
        text, keyboard = return_today_lessons(user_id)
    elif message_text == 'какие завтра пары?':
        text, keyboard = return_tomorrow_lessons(user_id)
    elif str(message_text[:3]).lower() == 'где' and message_text != 'где пара?':
        text, keyboard = return_where_is_the_classroom(user_id, message_text)
    else:
        request = message_text.lower()
        text = handler.find_message_value(request, user_id)
        if bool(text) == True:
            print(f'User: {user_id} send message: {message_text} at time: {time_now}')
        elif text == False:
            logging.basicConfig(filename="users_messages.log", level=logging.INFO)
            log_text = f'User: {user_id} send UNEXPECTED message: {message_text} at time: {time_now}'
            logging.info(log_text)
            text = texts_for_lesgaft_bot.invalid_text
            print(f'User: {user_id} send UNEXPECTED message: {message_text} at time: {time_now}')
    
    return text, keyboard
    

def change_group_step_1(chat_id):
    first_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    full_time = telebot.types.KeyboardButton('Очное обучение')
    part_time = telebot.types.KeyboardButton('Заочное обучение')
    first_step_keyboard.add(full_time, part_time)
    db_funcs_for_students_db.set_in_registration_process(chat_id, True)

    text = 'Какая у тебя форма обучения?'
    return text, first_step_keyboard

def change_group_step_2(chat_id, message_text):
    if db_funcs_for_students_db.get_state_of_registragion_process(chat_id) == False:
        text = 'Эта команда доступна только в процессе смены группы'
        return text, 'main_keyboard'
    
    second_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    undergraduate = telebot.types.KeyboardButton('Бакалавриат')
    magistracy = telebot.types.KeyboardButton('Магистратура')
    second_step_keyboard.add(undergraduate, magistracy)
    db_funcs_for_students_db.save_education_form(chat_id, message_text)
    
    text = 'На каком направлении ты учишься?'
    return text, second_step_keyboard

def change_group_step_3(chat_id, message_text):
    if db_funcs_for_students_db.get_state_of_registragion_process(chat_id) == False:
            text = 'Эта команда доступна только в процессе смены группы'
            return text, 'main_keyboard'

    db_funcs_for_students_db.save_academic_degree(chat_id, message_text)
    third_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    if message_text == 'бакалавриат':
        course_1 = telebot.types.KeyboardButton('1 курс')
        course_2 = telebot.types.KeyboardButton('2 курс')
        course_3 = telebot.types.KeyboardButton('3 курс')
        course_4 = telebot.types.KeyboardButton('4 курс')
        third_step_keyboard.add(course_1, course_2, course_3, course_4)
    elif message_text == 'магистратура':
        course_1 = telebot.types.KeyboardButton('1 курс')
        course_2 = telebot.types.KeyboardButton('2 курс')
        third_step_keyboard.add(course_1, course_2)
    
    text = 'На каком курсе ты учишься?'
    return text, third_step_keyboard

def change_group_step_4(chat_id, message_text):
    if db_funcs_for_students_db.get_state_of_registragion_process(chat_id) == False:
        text = 'Эта команда доступна только в процессе смены группы'
        return text, 'main_keyboard'
            
    db_funcs_for_students_db.save_number_of_course(chat_id, message_text)
    fourth_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    academic_degree = db_funcs_for_students_db.get_academic_degree(chat_id)
    if academic_degree == 'бакалавриат':
        if message_text == '1 курс':
            first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_lovs_1)
            second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_zovs_1)
        elif message_text == '2 курс':
            first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_lovs_2)
            second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_zovs_2)
        elif message_text == '3 курс':
            first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_lovs_3)
            second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_zovs_3)
        elif message_text == '4 курс':
            first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_lovs_4)
            second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_zovs_4)
        third_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_imst)
    elif academic_degree == 'магистратура':
        first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag)
        second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_afk)
        third_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_tour)
    fourth_step_keyboard.add(first_timetable, second_timetable, third_timetable)
    
    text = 'Как называется твоё расписание на сайте?'
    return text, fourth_step_keyboard
