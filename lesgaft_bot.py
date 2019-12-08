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
        message_text = texts_for_lesgaft_bot.greeting_text
        bot.send_message(message.from_user.id, message_text)

@bot.message_handler(content_types=["text"])
def main_func(message):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    main_keyboard.add(item1, item2, item3)

    if len(message.text) == 3 and message.text.isdigit():
        text = only_students_db.overwrite_group(message.text, message.from_user.id)        
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text == 'Какие сегодня пары?':
        text = today_and_tomorrow_lessons.return_today_lessons(message.from_user.id)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text == 'Какие завтра пары?':        
        text = today_and_tomorrow_lessons.return_tomorrow_lessons(message.from_user.id)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif str(message.text[:3]).lower() == 'где' and message.text.lower() != 'где пара?':
        text = time_class_and_location.return_location_of_class(message.from_user.id, message.text)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    elif message.text.lower() == 'где пара?':
        text = time_class_and_location.return_time_class_location(message.from_user.id)
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
    else:
        text = texts_for_lesgaft_bot.invalid_text
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        print('User: ' + str(message.from_user.id) + ' send message ' + str(message.text))

if __name__ == '__main__':
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    log = logging.getLogger("ex")
    try:
        bot.polling(none_stop=False)
    except:
        print('ERRORERRORERROR')
        bot.send_message(206171081, 'Я умер')
        log.exception('Error!')
