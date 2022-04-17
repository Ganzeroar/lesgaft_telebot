# -*- coding: utf-8 -*-

import telebot
import time
import logging
import os

import config
import db_funcs_for_students_db
import texts_for_lesgaft_bot
import request_handler
import excel_validator

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


def send_newsletter_to_subscribers(text):
    users_id = return_subscribed_to_news_users()
    for user_id in users_id:
        try:
            bot.send_message(user_id[0], text)
            print(f'message was sended to {user_id[0]}')
            time.sleep(0.1)
        except Exception as exception:
            time.sleep(0.1)
            print(exception)
            print(user_id)


def return_subscribed_to_news_users():
    subscribed_users = db_funcs_for_students_db.get_subscribed_to_newsletter_users()
    print(subscribed_users)
    return subscribed_users


@bot.message_handler(commands=['start'])
def start_message(message):
    text, keyboard = request_handler.create_start_stage()
    if db_funcs_for_students_db.user_already_in_db(message.from_user.id):
        text = 'С возвращением!'
    else:
        db_funcs_for_students_db.starting_insert_data(int(message.chat.id), str(
            message.from_user.first_name), str(message.from_user.last_name), int(message.date))
    try:
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    except Exception as exception:
        print('\n50\nОшибка в стартовой функции\n')
        print(exception)


@bot.message_handler(content_types=["text"])
def handle_request_and_send_answer(message):
    text, keyboard = request_handler.main_request_handler(
        message.text, message.from_user.id)
    if db_funcs_for_students_db.user_already_in_db(message.from_user.id) == False:
        db_funcs_for_students_db.starting_insert_data(int(message.chat.id), str(
            message.from_user.first_name), str(message.from_user.last_name), int(message.date))
    
    try:
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    except Exception as exception:
        print(
            f'Exception with send message to user = {str(message.from_user.id)} | {exception}')

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        path = os.path.abspath(os.path.dirname(__file__))
        path_2 = os.path.join(path, 'time_tables')
        path_3 = os.path.join(path_2, 'documents_for_validate')
        path_4 = os.path.join(path_3, message.document.file_name)
        with open(path_4, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Сканирование запущено")
        obj = excel_validator.Excel_validator()
        result = obj.run_validator('documents_for_validate')
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, e)

def main_run():
    try:
        bot.infinity_polling()
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
