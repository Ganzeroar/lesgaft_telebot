# -*- coding: utf-8 -*-

import telebot
import time
import logging
import datetime
import pytz

import config
import db_funcs_for_students_db
import texts_for_lesgaft_bot
import find_time_and_location
import find_lessons_at_date
import handler_of_unusual_requests as handler

bot = telebot.TeleBot(config.token)

def send_custom_message_to_user(user_id, text):
    try:
        user_id = int(user_id)
        text = str(text)
    except:
        print('Error with sending')
        return 
    bot.send_message(user_id, text)

def send_message_to_all_users(text):
    users = db_funcs_for_students_db.get_all_users()
    for user_id in users:
        try:
            bot.send_message(user_id[0], text)
            print(f'message was sended to {user_id}')
            time.sleep(0.1)
        except Exception as exception:
            time.sleep(0.1)
            print(exception)
            print(user_id)

def change_group_old(user_id, message_text):
    text = db_funcs_for_students_db.overwrite_group(message_text, user_id)
    return text, 'main_keyboard'

def return_where_is_the_lesson(chat_id):
    text = find_time_and_location.return_time_before_class_and_location(chat_id)
    return text, 'main_keyboard'

def return_today_lessons(chat_id):
    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    text = find_lessons_at_date.return_lessons_at_date(chat_id, time_now)
    return text, 'main_keyboard'

def return_tomorrow_lessons(chat_id):
    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    tomorrow = time_now + datetime.timedelta(days=1)
    text = find_lessons_at_date.return_lessons_at_date(chat_id, tomorrow)
    return text, 'main_keyboard'

def return_where_is_the_classroom(chat_id, message_text):
    text = find_time_and_location.return_location_of_class(chat_id, message_text)
    return text, 'main_keyboard'

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

@bot.message_handler(commands=['start'])
def start_message(message):

    if db_funcs_for_students_db.user_already_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, 'С возвращением!')
    else:
        db_funcs_for_students_db.starting_insert_data(int(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), int(message.date))
        text = texts_for_lesgaft_bot.greeting_text
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in greeting' 
            print(text_for_error)
        try:
            bot.send_message(message.from_user.id, text)
        except Exception as exception:
            print(exception)

@bot.message_handler(content_types=["text"])
def main_func(message):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    
    main_keyboard.add(item1, item2, item3)

    message_text = message.text.lower()

    timtetables_names = texts_for_lesgaft_bot.timetables_names

    # Если пользователь будет выходить из регистраци раньше чем она закончится - проверять в 
    # каждой функции и писать ему что бы он закончил
    # не забыть обновить базу 

    if len(message.text) == 3 and message.text.isdigit():
        text, keyboard = change_group_old(message.from_user.id, message.text)
    elif message_text == 'где пара?':
        text, keyboard = return_where_is_the_lesson(message.from_user.id)
    elif message_text == 'какие сегодня пары?':
        text, keyboard = return_today_lessons(message.from_user.id)
    elif message_text == 'какие завтра пары?':
        text, keyboard = return_tomorrow_lessons(message.from_user.id)
    elif str(message.text[:3]).lower() == 'где' and message_text != 'где пара?':
        text, keyboard = return_where_is_the_classroom(message.from_user.id, message_text)
    elif message_text == 'изменить группу3213':
        text, keyboard = change_group_step_1(message.from_user.id)    
    elif message_text == 'очное обучение' or message_text == 'заочное обучение':
        text, keyboard = change_group_step_2(message.from_user.id, message_text)
    elif message_text == 'бакалавриат' or message_text == 'магистратура':
        text, keyboard = change_group_step_3(message.from_user.id, message_text)
    elif message_text == '1 курс' or message_text == '2 курс' or message_text == '3 курс' or message_text == '4 курс':
        text, keyboard = change_group_step_4(message.from_user.id, message_text)
    # Идея: сделать автоматическую рассылку расписание, сделать так что бы время можно
    # было настроиить какой-то командй  


    #elif message_text in timtetables_names:
    #    if db_funcs_for_students_db.get_state_of_registragion_process(chat_id) == False:
    #        text = 'Эта команда доступна только в процессе смены группы'
    #        bot.send_message(message.from_user.id, 'text', reply_markup = main_keyboard)
    #        return
    #    
    #    # пользователю по ID в базе присвоить в колонку расписание (текст с сайта)
    #    db_funcs_for_students_db.save_timetable_name(message.from_user.id, message_text)
        
        
        # у кого нет групп - отдавать список направлений. Как вариант - создать ещё одну базу, куда
        # записывать у кого группы, а у кого направления 
        # обращение в базу, возвращение списка всех групп
        # сделать кнопки каждой группы из списка
        # прислать эти кноки 
        # следующая функция-обработчик - копия самой первой, только без ограничения
        
        
    #elif len(message.text) <= 3 and message.text.isdigit():
    #    if db_funcs_for_students_db.get_state_of_registragion_process(chat_id) == False:
    #        text = 'Эта команда доступна только в процессе смены группы'
    #        bot.send_message(message.from_user.id, 'text', reply_markup = main_keyboard)
    #        return  
    #    
    #    # если всё пройдёт успешно - снять из базы IN-registration_process
#
    #    text = db_funcs_for_students_db.overwrite_group(message.text, message.from_user.id)
    #    bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    
    else:
        request = message.text.lower()
        text = handler.find_message_value(request, message.from_user.id)
        keyboard = 'main_keyboard'
        if bool(text) == True:
            print(f'User: {message.from_user.id} send message: {message.text} at time: {message.date}')
            #bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif text == False:
            logging.basicConfig(filename="users_messages.log", level=logging.INFO)
            log_text = f'User: {message.from_user.id} send UNEXPECTED message: {message.text} at time: {message.date}'
            logging.info(log_text)
            text = texts_for_lesgaft_bot.invalid_text
            print(f'User: {message.from_user.id} send UNEXPECTED message: {message.text} at time: {message.date}')
    if keyboard == 'main_keyboard':
        keyboard = main_keyboard
    try:
        bot.send_message(message.from_user.id, text, reply_markup = keyboard)
    except:
        print('bot was blocked by user - ' + str(message.from_user.id))

def main_run():
    try:
        bot.polling(none_stop=False)
    except:
        time.sleep(60)
        logging.basicConfig(filename="sample.log", level=logging.INFO)
        log = logging.getLogger("ex")
        print('ERROR')
        bot.send_message(206171081, 'Я умер')
        log.exception('Error!')
        main_run()

if __name__ == '__main__':
    main_run()