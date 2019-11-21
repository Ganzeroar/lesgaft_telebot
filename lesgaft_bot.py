# -*- coding: utf-8 -*-

import config
import telebot
import lesgaft_bot_db
import texts_for_lesgaft_bot
import other_functions_for_bot
import subjects_db
import datetime
import time
import pytz
import logging


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):

    if lesgaft_bot_db.user_already_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, 'С возвращением!')
    else:
        lesgaft_bot_db.starting_insert_data(int(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), int(message.date))
        message_text = texts_for_lesgaft_bot.greeting_text
        bot.send_message(message.from_user.id, message_text)
        

@bot.message_handler(content_types=["text"])
def main_func(message):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Когда на учёбу?')
    main_keyboard.add(item1, item2, item3)

    msc_timezone = pytz.timezone('Europe/Moscow')

    if len(message.text) == 3 and message.text.isdigit():
        number_of_group = int(message.text)
        lesgaft_bot_db.update_group(message.from_user.id, number_of_group)
        text = f'Ваша группа {number_of_group} записана!' +  texts_for_lesgaft_bot.group_saved
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        print('User: ' + str(message.from_user.id) +  ' changed his group to ' + str(number_of_group))

    elif message.text == 'Какие сегодня пары?':
        time_now = datetime.datetime.now(tz=msc_timezone)
        day_of_week = other_functions_for_bot.return_russian_day_of_week(str(time_now.strftime('%a')))
        if day_of_week == 'воскресенье':
            bot.send_message(message.from_user.id, 'Сегодня воскресенье, не учимся!', reply_markup = main_keyboard)
            return
        try:
            number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
        except:
            bot.send_message(message.from_user.id, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.', reply_markup = main_keyboard)
            return
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        if db_name == None:
            bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup = main_keyboard)
        else:
            today_date = str(time_now.day) + '.' + str(time_now.month) + '.'
            today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
            if today_subjects == False:
                bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup = main_keyboard)
            else:
                message_text = ''
                list_of_times = ['9:45-11:15 \n', '11:30-13:30 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
                number_of_date = time_now.strftime("%d.%m.%Y.")
                message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
                try:
                    for x in range(5):
                        message_text += list_of_times[x] + today_subjects[x][0] + '\n\n'
                    bot.send_message(message.from_user.id, message_text, reply_markup = main_keyboard)
                    print('User: ' + str(message.from_user.id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
                except Exception as exception:
                    print(exception)
                    bot.send_message(message.from_user.id, texts_for_lesgaft_bot.error, reply_markup = main_keyboard)

    elif message.text == 'Какие завтра пары?':
        time_now = datetime.datetime.now(tz=msc_timezone)
        tomorrow = time_now + datetime.timedelta(days=1)
        day_of_week = other_functions_for_bot.return_russian_day_of_week(str(tomorrow.strftime('%a')))
        if day_of_week == 'воскресенье':
            bot.send_message(message.from_user.id, 'Завтра воскресенье, не учимся!', reply_markup = main_keyboard)
            return
        try:
            number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
        except:
            bot.send_message(message.from_user.id, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.', reply_markup = main_keyboard)
            return
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        if db_name == None:
            bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup = main_keyboard)

        else:
            tomorrow_date = str(time_now.day + 1) + '.' + str(time_now.month) + '.'
            tomorrow_subjects = subjects_db.get_subjects_today(name_of_group, db_name, tomorrow_date)
            if tomorrow_subjects == False:
                bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup = main_keyboard)
            else:
                message_text = ''
                list_of_times = ['9:45-11:15 \n', '11:30-13:00 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
                number_of_date = tomorrow.strftime("%d.%m.%Y.")
                message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
                try:
                    for x in range(5):
                        message_text += list_of_times[x] + tomorrow_subjects[x][0] + '\n\n'
                    bot.send_message(message.from_user.id, message_text, reply_markup = main_keyboard)
                    print('User: ' + str(message.from_user.id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
                except Exception as exception:
                    print(exception)
                    bot.send_message(message.from_user.id, texts_for_lesgaft_bot.error, reply_markup = main_keyboard)

    elif message.text == 'Где пара?':
        
        
        if other_functions_for_bot.is_time_between(datetime.time(00,00), datetime.time(9,44)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 0)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(9,45), datetime.time(11,15)):
            text = other_functions_for_bot.return_message_text_about_current_lesson(message.from_user.id, 0)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(11,16), datetime.time(11,29)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 1)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(11,30), datetime.time(13,00)):
            text = other_functions_for_bot.return_message_text_about_current_lesson(message.from_user.id, 1)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(13,1), datetime.time(13,29)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 2)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(13,30), datetime.time(15,00)):
            text = other_functions_for_bot.return_message_text_about_current_lesson(message.from_user.id, 2)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(15,1), datetime.time(15,14)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 3)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(15,15), datetime.time(16,45)):
            text = other_functions_for_bot.return_message_text_about_current_lesson(message.from_user.id, 3)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(16,46), datetime.time(16,59)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 4)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(17,00), datetime.time(18,30)):
            text = other_functions_for_bot.return_message_text_about_current_lesson(message.from_user.id, 4)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        elif other_functions_for_bot.is_time_between(datetime.time(18,31), datetime.time(23,59)):
            text = other_functions_for_bot.return_message_text_to_about_time_before_lesson(message.from_user.id, 5)
            bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)

        print('User: ' + str(message.from_user.id) +  ' from ' + str(number_of_group) + ' ask about where the lesson' )



        # высчитать время, узнать какая сейчас и какая следующая
        # спростить базу, оставить только название пары
        # спросить базу, узнать о местонахождении

    else:
        text = texts_for_lesgaft_bot.invalid_text
        bot.send_message(message.from_user.id, text, reply_markup = main_keyboard)
        print('User: ' + str(message.from_user.id) + ' send message ' + str(message.text))

logging.basicConfig(filename="sample.log", level=logging.INFO)
log = logging.getLogger("ex")
if __name__ == '__main__':
    try:
        bot.polling(none_stop=False)
    except:
        print('ERRORERRORERROR')
        bot.send_message(206171081, 'Я умер')
        log.exception('Error!')
