# -*- coding: utf-8 -*-

import config
import telebot
import lesgaft_bot_db
import subjects_db
import datetime


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    message_text = """Привет, пока что я поддерживаю только расписание ЗОВС. 
                    А теперь напиши номер своей группы числом. Будь аккуратен и не ошибись. 
                    Если введёшь что-то не верно или захочешь поменять группу - напиши '/reconf *новый номер группы*'"""
    bot.send_message(message.chat.id, message_text)
    print(message.text)

@bot.message_handler(content_types=["text"])
def main_func(message):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_keyboard.row('Сегодня', 'Завтра')
    if len(message.text) == 3 and message.text.isdigit():
        if lesgaft_bot_db.user_already_in_db(message.chat.id) == True:
            bot.send_message(message.from_user.id, 'Так нельзя. Не читал правила? Для изменения группы воспользуйся специальной командой.')
        else:
            group_number = int(message.text)
            student_info = [(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.date, group_number)]
            lesgaft_bot_db.starting_insert_data(student_info)

            #main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            #main_keyboard.row('Сегодня', 'Завтра')
            bot.send_message(message.from_user.id, 'Теперь выбери что-нибудь', reply_markup=main_keyboard)

    elif message.text == 'Сегодня':
        time_now = datetime.datetime.now()
        number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
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
                list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
                for x in range(5):
                    message_text += list_of_times[x] + ' : ' + today_subjects[x][0] + '\n'

                bot.send_message(message.from_user.id, message_text)

    elif message.text == 'Завтра':
        time_now = datetime.datetime.now()
        number_of_group = lesgaft_bot_db.get_group_number(message.from_user.id)[0][0]
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        if db_name == None:
            bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
        else:
            today_date = str(time_now.day + 1) + '.' + str(time_now.month) + '.'
            today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
            if today_subjects == False:
                bot.send_message(message.from_user.id, 'Твоей группы не существует. Измени номер группы.', reply_markup=main_keyboard)
            else:
                message_text = ''
                list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
                print(today_subjects)
                try:
                    for x in range(5):
                        message_text += list_of_times[x] + ' : ' + today_subjects[x][0] + '\n'
                    bot.send_message(message.from_user.id, message_text)
                except Exception as exception:
                    print(exception)
                    bot.send_message(message.from_user.id, 'Если ты видишь это сообщение, значит что-то сломалось по причине ВЕЛИКОЛЕПНОГО заполнения нашего ЛУЧШЕГО В МИРЕ расписания САМЫМИ ВНИМАТЕЛЬНЫМИ, СООБРАЗИТЕЛЬНЫМИ И УМНЫМИ работниками университета. Пожалуйста, напиши мне на почту ganzeroar@gmail.com номер группы, дату и время, когда ты пытался получить расписание и увидел это сообщение.')

    elif '/reconf' in message.text:
        group_number_text = message.text[-3:]
        if len(group_number_text) == 3 and group_number_text.isdigit():
            group_number = int(group_number_text)
            
            lesgaft_bot_db.update_group(message.from_user.id, group_number)
            bot.send_message(message.from_user.id, 'Теперь выбери что-нибудь', reply_markup=main_keyboard)
        else:
            bot.send_message(message.from_user.id, 'Возможно в твоём вводе ошибка. Попробуй ешё раз.', reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, 'Возможно в твоём вводе ошибка. Попробуй ешё раз.', reply_markup=main_keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    
    if call.data == 'week':
        None
        
    elif call.data == 'today':
        number_of_group = lesgaft_bot_db.get_group_number(call.from_user.id)[0][0]
        name_of_group = 'Группа_' + str(number_of_group)
        db_name = subjects_db.get_db_name(number_of_group)
        today_date = str(time_now.day) + '.' + str(time_now.month) + '.'
        today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
        
        message_text = ''
        list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
        for x in range(5):
            message_text += list_of_times[x] + ' : ' + today_subjects[x][0] + '\n'
        
        bot.send_message(call.from_user.id, message_text)

        print(today_subjects)
    elif call.data == 'now':
        print('now')

    
    

if __name__ == '__main__':
    bot.polling(none_stop=True)
