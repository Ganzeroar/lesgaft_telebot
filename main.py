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
import request_handler

bot = telebot.TeleBot(config.token)

def send_custom_message_to_user(user_id, text):
    try:
        user_id = int(user_id)
        text = str(text)
        bot.send_message(user_id, text)
    except:
        print('Error with sending')
        return 

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

@bot.message_handler(commands=['start'])
def start_message(message):
    text = ''
    if db_funcs_for_students_db.user_already_in_db(message.from_user.id):
        text = 'С возвращением!'
    else:
        db_funcs_for_students_db.starting_insert_data(int(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), int(message.date))
        text = texts_for_lesgaft_bot.greeting_text
    try:
        bot.send_message(message.from_user.id, text)
    except Exception as exception:
        print('\n50\n')
        print(exception)

@bot.message_handler(content_types=["text"])
def main_func(message):
    text, keyboard = request_handler.main_request_handler(message.text, message.from_user.id)
    try:
        bot.send_message(message.from_user.id, text, reply_markup = keyboard)
    except Exception as exception:
        print(f'Exception with send message to user = {str(message.from_user.id)} | {exception}')

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