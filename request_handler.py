import telebot
import time
import logging
import datetime
import pytz

import db_funcs_for_students_db
import db_funcs_for_subjects_db
import texts_for_lesgaft_bot
import find_time_and_location
import find_lessons_at_date
import handler_of_unusual_requests as handler


def change_group_old(user_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    text = db_funcs_for_students_db.overwrite_group(message_text, user_id)
    return text, main_keyboard


def return_where_is_the_lesson(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)
    text = find_time_and_location.return_time_before_class_and_location(
        chat_id)
    return text, main_keyboard


def return_today_lessons(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    text = find_lessons_at_date.return_lessons_at_date(chat_id, time_now)
    return text, main_keyboard


def return_tomorrow_lessons(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    tomorrow = time_now + datetime.timedelta(days=1)
    text = find_lessons_at_date.return_lessons_at_date(chat_id, tomorrow)
    return text, main_keyboard


def return_where_is_the_classroom(chat_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    text = find_time_and_location.return_location_of_class(
        chat_id, message_text)
    return text, main_keyboard


def go_to_timetables_stage():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    text = texts_for_lesgaft_bot.go_to_timetables_stage_text
    return text, main_keyboard


def create_start_stage():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Расписание')
    item2 = telebot.types.KeyboardButton('Настройки')
    item3 = telebot.types.KeyboardButton('Что умеет ЛесгафтБот')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.greeting_text
    return text, main_keyboard


def go_to_menu_stage():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Расписание')
    item2 = telebot.types.KeyboardButton('Настройки')
    item3 = telebot.types.KeyboardButton('Что умеет ЛесгафтБот')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.go_to_menu_stage_text
    return text, main_keyboard


def what_lesgaftbot_can_do():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Расписание')
    item2 = telebot.types.KeyboardButton('Настройки')
    item3 = telebot.types.KeyboardButton('Что умеет ЛесгафтБот')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.what_lesgaftbot_can_do_text
    return text, main_keyboard


def go_to_settings_stage():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Подписки и рассылки')
    item2 = telebot.types.KeyboardButton('Связь с разработчиком')
    item3 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.go_to_settings_stage_text
    return text, main_keyboard


def go_to_subscriptions_and_newsletters_stage(user_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    status = db_funcs_for_students_db.get_subscribe_in_newsletter_status(
        user_id)

    if status == False:
        item1 = telebot.types.KeyboardButton(
            'Подписаться на рассылку новостей')
    elif status == True:
        item1 = telebot.types.KeyboardButton('Отписаться от рассылки новостей')
    item2 = telebot.types.KeyboardButton('Информация о подписках')
    item3 = telebot.types.KeyboardButton('Вернуться в настройки')

    main_keyboard.add(item1, item2, item3, )

    text = texts_for_lesgaft_bot.go_to_subscriptions_and_newsletters_text
    return text, main_keyboard


def subscribe_user_to_newsletter(user_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    status = db_funcs_for_students_db.get_subscribe_in_newsletter_status(
        user_id)

    if status == False:
        print(f'User {user_id} subscribe to newsletter')
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(user_id, True)
        item1 = telebot.types.KeyboardButton('Отписаться от рассылки новостей')
        text = 'Подписка активирована'
    elif status == True:
        print(f'User {user_id} unsubscribe to newsletter')
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(user_id, False)
        item1 = telebot.types.KeyboardButton(
            'Подписаться на рассылку новостей')
        text = 'Подписка отключена'

    item2 = telebot.types.KeyboardButton('Информация о подписках')
    item3 = telebot.types.KeyboardButton('Вернуться в настройки')

    main_keyboard.add(item1, item2, item3)

    return text, main_keyboard


def info_about_subscriptions(user_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    status = db_funcs_for_students_db.get_subscribe_in_newsletter_status(
        user_id)

    if status == False:
        item1 = telebot.types.KeyboardButton(
            'Подписаться на рассылку новостей')
    elif status == True:
        item1 = telebot.types.KeyboardButton('Отписаться от рассылки новостей')
    item2 = telebot.types.KeyboardButton('Информация о подписках')
    item3 = telebot.types.KeyboardButton('Вернуться в настройки')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.info_about_subscriptions_text
    return text, main_keyboard


def communication_with_developer():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Подписки и рассылки')
    item2 = telebot.types.KeyboardButton('Связь с разработчиком')
    item3 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3)

    text = texts_for_lesgaft_bot.communication_with_developer_text
    return text, main_keyboard


def save_info_about_wrong_timetables(user_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    #item4 = telebot.types.KeyboardButton('Расписание неправильное')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    number_of_group = db_funcs_for_students_db.get_group_number(user_id)
    if number_of_group == False:
        text = 'Ошибка, группы нет в базе'
        return text, main_keyboard
    name_of_group = 'группа_' + str(number_of_group)
    db_name = db_funcs_for_subjects_db.get_db_name(name_of_group)
    if db_name == None or db_funcs_for_subjects_db.is_group_exist(name_of_group, db_name) == False:
        text = 'Ошибка, группы нет в базе'
        return text, main_keyboard

    name_of_group = db_funcs_for_subjects_db.return_new_group_name(
        name_of_group, db_name)
    subjects = db_funcs_for_subjects_db.get_subjects_today(
        name_of_group, db_name, time_now)
    number_of_date = time_now.strftime("%d.%m.%Y.")

    logging.basicConfig(
        filename="wrong_timetables_reports.log", level=logging.INFO)
    log_text = f'{name_of_group} {number_of_date}\n{subjects}\nЮзер: {user_id}'

    logging.info(log_text)

    print(f'User {user_id} report about wrong newsletters')

    text = texts_for_lesgaft_bot.wrong_timetables
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
    # elif message_text == 'расписание неправильное':
    #    text, keyboard = save_info_about_wrong_timetables(user_id)
    elif str(message_text[:3]).lower() == 'где' and message_text != 'где пара?':
        text, keyboard = return_where_is_the_classroom(user_id, message_text)
    elif message_text == 'вернуться в меню':
        print(f'User {user_id} return to menu')
        text, keyboard = go_to_menu_stage()
    elif message_text == 'настройки':
        print(f'User {user_id} go to settings')
        text, keyboard = go_to_settings_stage()
    elif message_text == 'вернуться в настройки':
        print(f'User {user_id} go to settings')
        text, keyboard = go_to_settings_stage()
    elif message_text == 'подписки и рассылки':
        print(f'User {user_id} go to subscriptions and newsletters stage')
        text, keyboard = go_to_subscriptions_and_newsletters_stage(user_id)
    elif message_text == 'что умеет лесгафтбот':
        print(f'User {user_id} ask what lesgaftbot can do')
        text, keyboard = what_lesgaftbot_can_do()
    elif message_text == 'информация о подписках':
        print(f'User {user_id} ask info about subsctibe')
        text, keyboard = info_about_subscriptions(user_id)
    elif message_text == 'связь с разработчиком':
        print(f'User {user_id} ask about communication with developer')
        text, keyboard = communication_with_developer()
    elif message_text == 'подписаться на рассылку новостей' or message_text == 'отписаться от рассылки новостей':
        text, keyboard = subscribe_user_to_newsletter(user_id)
    elif message_text == 'расписание':
        print(f'User {user_id} go to timetables')
        text, keyboard = go_to_timetables_stage()
    else:
        request = message_text.lower()
        text = handler.find_message_value(request, user_id)
        if bool(text) == True:
            print(
                f'User: {user_id} send message: {message_text} at time: {time_now.ctime()}')
        elif text == False:
            logging.basicConfig(
                filename="users_messages.log", level=logging.INFO)
            log_text = f'User: {user_id} send UNEXPECTED message: {message_text} at time: {time_now.ctime()}'
            logging.info(log_text)
            text = texts_for_lesgaft_bot.invalid_text
            print(
                f'User: {user_id} send UNEXPECTED message: {message_text} at time: {time_now.ctime()}')

    return text, keyboard
