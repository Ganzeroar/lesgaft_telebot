import telebot
import logging
import datetime
import pytz

import db_funcs_for_students_db
import texts_for_lesgaft_bot
import find_time_and_location
import find_lessons_at_date
import handler_of_unusual_requests as handler
import configurations


def change_group_old(user_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    item5 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item5)

    text = db_funcs_for_students_db.overwrite_group(message_text, user_id)
    return text, main_keyboard


def start_change_group_nonstandart(message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    if message_text == '405':
        item1 = telebot.types.KeyboardButton('ФОД, Водные виды спорта')
        item2 = telebot.types.KeyboardButton('Плавание II')
    elif message_text == '412':
        item1 = telebot.types.KeyboardButton('Самбо, Атлетизм')
        item2 = telebot.types.KeyboardButton(
            'Антидопинговое обеспечение в спорте, Танц.спорт, Спорт.акроб., Водные виды спорта, Академ. гребля,Гандбол,Волейбол,Легк. атл., Плавание')
    elif message_text == '413':
        item1 = telebot.types.KeyboardButton('Борьба, Дзюдо, Фехтование')
        item2 = telebot.types.KeyboardButton(
            'Менеджмент ФКиС, Худ. Гимн, Водные виды спорта, Водное поло Баскетбол')
    elif message_text == '328':
        item1 = telebot.types.KeyboardButton(
            'Спорт. аэробика Лёгк. атл. Теннис Плавание Футбол (антидопинг)')
        item2 = telebot.types.KeyboardButton(
            'Антидопинг (комп. спорт, тхэквондо, кикбоксинг, дартс, полиатлон, биатлон, фигурное катание, конькобежный спорт, пауэрлифтинг, гиревой спорт)')

    main_keyboard.add(item1, item2)

    text = 'Выбери свою специализацию'
    return text, main_keyboard


def start_change_group_327_step_1():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('ЛОВС')
    item2 = telebot.types.KeyboardButton('ЗОВС')

    main_keyboard.add(item1, item2)

    text = 'Выбери свой факультет'
    return text, main_keyboard


def start_change_group_327_step_2(message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)
    if message_text == 'ловс':
        item1 = telebot.types.KeyboardButton(
            'Направленность (профиль): Менеджмент ФКиС Футбол Волейбол Лёгк. атл. Плавание (менеджмент ФКиС)')
        item2 = telebot.types.KeyboardButton(
            'Направленность (профиль): ССиИ Плавание (ССиИ)')
    elif message_text == 'зовс':
        item1 = telebot.types.KeyboardButton(
            'Направленность (профиль): Менеджмент ФКиС Менеджмент (тхэквондо, дзюдо, кикбиксинг, скалолазание, керлинг, полиатлон, хоккей, дартс, фехтование)')
        item2 = telebot.types.KeyboardButton(
            'Направленность (профиль): ССиИ ССиИ (тхэквондо, дартс)')

    main_keyboard.add(item1, item2)

    text = 'Выбери свою специализацию'
    return text, main_keyboard


def change_group_nonstandart(user_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    item4 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item4)
    if message_text == 'фод, водные виды спорта':
        db_name = 'zovs_4'
        group_number = '405'
    elif message_text == 'плавание ii':
        db_name = 'lovs_4'
        group_number = '405'
    elif message_text == 'антидопинговое обеспечение в спорте, танц.спорт, спорт.акроб., водные виды спорта, академ. гребля,гандбол,волейбол,легк. атл., плавание':
        db_name = 'lovs_4'
        group_number = '412'
    elif message_text == 'самбо, атлетизм':
        db_name = 'zovs_4'
        group_number = '412'
    elif message_text == 'борьба, дзюдо, фехтование':
        db_name = 'zovs_4'
        group_number = '413'
    elif message_text == 'менеджмент фкис, худ. гимн, водные виды спорта, водное поло баскетбол':
        db_name = 'lovs_4'
        group_number = '413'
    elif message_text == 'спорт. аэробика лёгк. атл. теннис плавание футбол (антидопинг)':
        db_name = 'lovs_3'
        group_number = '328'
    elif message_text == 'антидопинг (комп. спорт, тхэквондо, кикбоксинг, дартс, полиатлон, биатлон, фигурное катание, конькобежный спорт, пауэрлифтинг, гиревой…':
        db_name = 'zovs_3'
        group_number = '328'

    text = db_funcs_for_students_db.save_timetable_name(
        user_id, db_name, group_number)
    return text, main_keyboard


def change_group_327(user_id, message_text):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
    item4 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2, item3, item4)

    if message_text == 'направленность (профиль): менеджмент фкис футбол волейбол лёгк. атл. плавание (менеджмент фкис)':
        db_name = 'lovs_3'
        group_name = 'направленность_профиль_менеджмент_фкис_футбол_волейбол_лёгк_атл_плавание_менеджмент_фкис_группа_327'
    elif message_text == 'направленность (профиль): ссии плавание (ссии)':
        db_name = 'lovs_3'
        group_name = 'направленность_профиль_ссии_плавание_ссии_группа_327'
    elif message_text == 'направленность (профиль): менеджмент фкис менеджмент (тхэквондо, дзюдо, кикбиксинг, скалолазание, керлинг, полиатлон, хоккей, дартс…':
        db_name = 'zovs_3'
        group_name = 'направленность_профиль_менеджмент_фкис_менеджмент_тхэквондо_дзюдо_кикбиксинг_скалолазание_керлинг_полиатлон_хоккей_дартс_фехтование_группа_327'
    elif message_text == 'направленность (профиль): ссии ссии (тхэквондо, дартс)':
        db_name = 'zovs_3'
        group_name = 'направленность_профиль_ссии_ссии_тхэквондо_дартс_группа_327'

    group_number = '327'

    text = db_funcs_for_students_db.save_timetable_name(
        user_id, db_name, group_number)
    db_funcs_for_students_db.save_education_form(user_id, group_name)
    return text, main_keyboard


def return_where_is_the_lesson(chat_id):
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Где пара?')
    item2 = telebot.types.KeyboardButton('Какие сегодня пары?')
    item3 = telebot.types.KeyboardButton('Какие завтра пары?')
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

    item1 = telebot.types.KeyboardButton('Связь с разработчиком')
    item2 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2)

    text = texts_for_lesgaft_bot.go_to_settings_stage_text
    return text, main_keyboard


def communication_with_developer():
    main_keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=1)

    item1 = telebot.types.KeyboardButton('Связь с разработчиком')
    item2 = telebot.types.KeyboardButton('Вернуться в меню')

    main_keyboard.add(item1, item2)

    text = texts_for_lesgaft_bot.communication_with_developer_text
    return text, main_keyboard


def main_request_handler(message_text, user_id):
    message_text = message_text.lower()

    time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    text, keyboard = '', ''
    if len(message_text) == 3 and message_text.isdigit():
        if message_text == '405' or message_text == '412' or message_text == '413' or message_text == '328':
            text, keyboard = start_change_group_nonstandart(message_text)
        elif message_text == '327':
            text, keyboard = start_change_group_327_step_1()
        else:
            text, keyboard = change_group_old(user_id, message_text)
    elif message_text == 'ловс' or message_text == 'зовс':
        text, keyboard = start_change_group_327_step_2(message_text)
    elif message_text == 'где пара?':
        text, keyboard = return_where_is_the_lesson(user_id)
    elif message_text == 'какие сегодня пары?':
        text, keyboard = return_today_lessons(user_id)
    elif message_text == 'какие завтра пары?':
        text, keyboard = return_tomorrow_lessons(user_id)
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
    elif message_text == 'что умеет лесгафтбот':
        print(f'User {user_id} ask what lesgaftbot can do')
        text, keyboard = what_lesgaftbot_can_do()
    elif message_text == 'связь с разработчиком':
        print(f'User {user_id} ask about communication with developer')
        text, keyboard = communication_with_developer()
    elif message_text == 'расписание':
        print(f'User {user_id} go to timetables')
        text, keyboard = go_to_timetables_stage()
    elif message_text in configurations.non_standart_group:
        text, keyboard = change_group_nonstandart(user_id, message_text)
    elif message_text in configurations.non_standart_group_327:
        text, keyboard = change_group_327(user_id, message_text)
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
