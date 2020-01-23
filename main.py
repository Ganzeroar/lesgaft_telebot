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
            time.sleep(1)
        except Exception as exception:
            time.sleep(1)
            print(exception)
            print(user_id)

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

    if len(message.text) == 3 and message.text.isdigit():
        text = db_funcs_for_students_db.overwrite_group(message.text, message.from_user.id)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text.lower() == 'где пара?':
        text = find_time_and_location.return_time_before_class_and_location(message.from_user.id)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in time and location at time {message.date}' 
            print(text_for_error)
            text = texts_for_lesgaft_bot.mystical_error_text
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text.lower() == 'какие сегодня пары?':
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        text = find_lessons_at_date.return_lessons_at_date(message.from_user.id, time_now)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text.lower() == 'какие завтра пары?':
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        tomorrow = time_now + datetime.timedelta(days=1)
        text = find_lessons_at_date.return_lessons_at_date(message.from_user.id, tomorrow)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif str(message.text[:3]).lower() == 'где' and message.text.lower() != 'где пара?':
        message_text = message.text.lower()
        text = find_time_and_location.return_location_of_class(message.from_user.id, message_text)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    else:
        request = message.text.lower()
        text = handler.find_message_value(request, message.from_user.id)
        if bool(text) == True:
            print(f'User: {message.from_user.id} send message: {message.text} at time: {message.date}')
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif text == False:
            logging.basicConfig(filename="users_messages.log", level=logging.INFO)
            log_text = f'User: {message.from_user.id} send UNEXPECTED message: {message.text} at time: {message.date}'
            logging.info(log_text)
            bot.send_message(message.from_user.id, texts_for_lesgaft_bot.invalid_text, reply_markup = main_keyboard)
            print(f'User: {message.from_user.id} send UNEXPECTED message: {message.text} at time: {message.date}')

def main_run():
    try:
        bot.polling(none_stop=False)
    except:
        logging.basicConfig(filename="sample.log", level=logging.INFO)
        log = logging.getLogger("ex")
        print('ERROR')
        bot.send_message(206171081, 'Я умер')
        log.exception('Error!')
        main_run()

if __name__ == '__main__':
    main_run()