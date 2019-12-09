# -*- coding: utf-8 -*-

import telebot
import time
import logging

import config
import only_students_db
import texts_for_lesgaft_bot
import time_class_and_location
import today_and_tomorrow_lessons

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):

    if only_students_db.user_already_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, 'С возвращением!')
    else:
        only_students_db.starting_insert_data(int(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), int(message.date))
        text = texts_for_lesgaft_bot.greeting_text
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in greeting' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text)

@bot.message_handler(content_types=["text"])
def main_func(message):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    main_keyboard.add(item1, item2, item3)

    if len(message.text) == 3 and message.text.isdigit():
        text = only_students_db.overwrite_group(message.text, message.from_user.id)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in overwrite' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text == 'Какие сегодня пары?':
        text = today_and_tomorrow_lessons.return_today_lessons(message.from_user.id)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in today lessons' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text == 'Какие завтра пары?':        
        text = today_and_tomorrow_lessons.return_tomorrow_lessons(message.from_user.id)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in tomorrow lessons' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif str(message.text[:3]).lower() == 'где' and message.text.lower() != 'где пара?':
        text = time_class_and_location.return_location_of_class(message.from_user.id, message.text)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in location of class' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text.lower() == 'где пара?':
        text = time_class_and_location.return_time_class_location(message.from_user.id)
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in time and location' 
            print(text_for_error)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    else:
        text = texts_for_lesgaft_bot.invalid_text
        if text == None or text == False or bool(text) == False or text == [] or text == [[]] or text == {} or text == '':
            text_for_error = f'ERRORERRORERROR User: {message.from_user.id} send message: {message.text} and get the text for answer: {text} in invalid text' 
            print(text_for_error)

        logging.basicConfig(filename="users_messages.log", level=logging.INFO)
        log_text = f'User: {message.from_user.id} send message: {message.text} at time: {message.date}'
        logging.info(log_text)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        print(f'User: {message.from_user.id} send message: {message.text} at time: {message.date}')

if __name__ == '__main__':
    try:
        bot.polling(none_stop=False)
    except:
        logging.basicConfig(filename="sample.log", level=logging.INFO)
        log = logging.getLogger("ex")
        print('ERRORERRORERROR')
        bot.send_message(206171081, 'Я умер')
        log.exception('Error!')
