# -*- coding: utf-8 -*-

import config
import telebot
import lesgaft_bot_db
import texts_for_lesgaft_bot
import other_functions_for_bot
import subjects_db
import datetime
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
    #item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Когда на учёбу?')
    main_keyboard.add(item2, item3)

    msc_timezone = pytz.timezone('Europe/Moscow')

    if len(message.text) == 3 and message.text.isdigit():
        number_of_group = int(message.text)
        lesgaft_bot_db.update_group(message.from_user.id, number_of_group)
        text = f'Ваша группа {number_of_group} записана!' +  texts_for_lesgaft_bot.group_saved
        bot.send_message(message.from_user.id, text, reply_markup=main_keyboard)
        print('User: ' + str(message.from_user.id) +  ' changed his group to ' + str(number_of_group))

    elif message.text == 'Какие сегодня пары?':
        time_now = datetime.datetime.now(tz=msc_timezone)
        day_of_week = other_functions_for_bot.return_russian_day_of_week(str(time_now.strftime('%a')))
        if day_of_week == 'воскресенье':
            bot.send_message(message.from_user.id, 'Сегодня воскресенье, не учимся!')
            return
        try:
            number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
        except:
            bot.send_message(message.from_user.id, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.', reply_markup=main_keyboard)
            return
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        if db_name == None:
            bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
        else:
            today_date = str(time_now.day) + '.' + str(time_now.month) + '.'
            today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
            if today_subjects == False:
                bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
            else:
                message_text = ''
                list_of_times = ['9:45-11:15 \n', '11:30-13:30 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
                number_of_date = time_now.strftime("%d.%m.%Y.")
                message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
                try:
                    for x in range(5):
                        message_text += list_of_times[x] + today_subjects[x][0] + '\n\n'
                    bot.send_message(message.from_user.id, message_text)
                    print('User: ' + str(message.from_user.id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
                except Exception as exception:
                    print(exception)
                    bot.send_message(message.from_user.id, texts_for_lesgaft_bot.error)

    elif message.text == 'Какие завтра пары?':
        time_now = datetime.datetime.now(tz=msc_timezone)
        tomorrow = time_now + datetime.timedelta(days=1)
        day_of_week = other_functions_for_bot.return_russian_day_of_week(str(tomorrow.strftime('%a')))
        if day_of_week == 'воскресенье':
            bot.send_message(message.from_user.id, 'Завтра воскресенье, не учимся!')
            return
        try:
            number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
        except:
            bot.send_message(message.from_user.id, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.', reply_markup=main_keyboard)
            return
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        if db_name == None:
            bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
        else:
            tomorrow_date = str(time_now.day + 1) + '.' + str(time_now.month) + '.'
            tomorrow_subjects = subjects_db.get_subjects_today(name_of_group, db_name, tomorrow_date)
            if tomorrow_subjects == False:
                bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
            else:
                message_text = ''
                list_of_times = ['9:45-11:15 \n', '11:30-13:30 \n', '13:30-15:00 \n', '15:15-16:45 \n', '17:00-18:30 \n']
                number_of_date = tomorrow.strftime("%d.%m.%Y.")
                message_text += f'Расписание на {day_of_week} ({number_of_date}) \n\n'
                try:
                    for x in range(5):
                        message_text += list_of_times[x] + tomorrow_subjects[x][0] + '\n\n'
                    bot.send_message(message.from_user.id, message_text)
                    print('User: ' + str(message.from_user.id) +  ' from ' + str(number_of_group) + ' ask about ' + str(number_of_date))
                except Exception as exception:
                    print(exception)
                    bot.send_message(message.from_user.id, texts_for_lesgaft_bot.error)

    #elif message.text == 'Где пара?':
    #    time_now = datetime.datetime.now()
    #    print(time_now)
    #    time_now = datetime.datetime.utcnow().time()
    #    print(time_now)
    #    hour_now = int(time_now.strftime('%H'))
    #    minute_now = int(time_now.strftime('%M'))
    #    
#
    #    def is_time_between(begin_time, end_time, check_time=None):
    #        # If check time is not given, default to current UTC time
    #        check_time = check_time or datetime.datetime.utcnow().time()
    #        if begin_time < end_time:
    #            return check_time >= begin_time and check_time <= end_time
    #        else: # crosses midnight
    #            return check_time >= begin_time or check_time <= end_time
#
    #    # Original test case from OP
    #    print(is_time_between(datetime.time(10,30), datetime.time(16,30)))
#
#
    #    print(time_now.strftime('%H : %M'))

        # высчитать время, узнать какая сейчас и какая следующая
        # спростить базу, оставить только название пары
        # спросить базу, узнать о местонахождении

    else:
        text = texts_for_lesgaft_bot.invalid_text
        bot.send_message(message.from_user.id, text, reply_markup=main_keyboard)
        print('User: ' + str(message.from_user.id) + ' send message ' + str(message.text))

logging.basicConfig(filename="sample.log", level=logging.INFO)
log = logging.getLogger("ex")
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        print('ERRORERRORERROR')
        log.exception('Error!')
