# -*- coding: utf-8 -*-

import datetime
import pytz
import find_lessons_at_date
import texts_for_lesgaft_bot

def next_weekday(weekday):
    #0 - monday
    #1 - tuesday etc.
    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = datetime.datetime.now(tz=msc_timezone)

    day = date_and_time_now.day
    mounh = date_and_time_now.month
    year = date_and_time_now.year
    date = datetime.date(year, mounh, day)

    days_ahead = weekday - date.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return date + datetime.timedelta(days_ahead)

monday_lessons_requests = ['какие в понедельник пары','какие в понедельник пары?',
    'какие в понедельник пары ?','какие пары в понедельник','какие пары в понедельник?',
    'какие пары в понедельник ?','расписание на понедельник','понедельник',
    'пары в понедельник', 'пары на понедельник', 'какое расписание в понедельник',
    'предметы в понедельник', 'расписание в понедельник', 'предметы в понедельник?', 
    'на понедельник', 'какое расписание в понедельник', 'расписание понедельник',
    'какие пары на понедельник', 'какие пары на понедельник?', 
    'какие пары на понедельник ?', 'расписание на понедельник?', 
    'расписание на понедельник ?']

tuesday_lessons_requests = ['какие во вторник пары','какие во вторник пары?',
    'какие во вторник пары ?','какие пары во вторник','какие пары во вторник?',
    'какие пары во вторник ?','расписание на вторник','вторник',
    'пары во вторник', 'пары на вторник', 'какое расписание во вторник', 
    'предметы во вторник', 'расписание во вторник', 'расписание в вторник', 
    'предметы во вторник?', 'на вторник', 'какое расписание во вторник',
    'расписание вторник', 'какие пары на вторник', 'какие пары на вторник?'
    , 'какие пары на вторник ?', 'расписание на вторник?', 'расписание на вторник ?']

wednesday_lessons_requests = ['какие в среду пары','какие в среду пары?',
    'какие в среду пары ?','какие пары в среду','какие пары в среду?',
    'какие пары в среду ?','расписание на среду','среда','пары в среду', 
    'пары на среду', 'какое расписание в среду', 'предметы в среду', 
    'расписание в среду', 'предметы в среду?', 'на среду', 
    'какое расписание в среду', 'расписание среда', 'какие пары на среду', 
    'какие пары на среду?', 'какие пары на среду ?', 'расписание на среду?', 
    'расписание на среду ?']

thursday_lessons_requests = ['какие в четверг пары','какие в четверг пары?',
    'какие в четверг пары ?','какие пары в четверг','какие пары в четверг?',
    'какие пары в четверг ?','расписание на четверг','четверг',
    'пары в четверг', 'пары на четверг', 'какое расписание в четверг',
    'предметы в четверг', 'расписание в четверг', 'предметы в четверг?', 
    'на четверг', 'какое расписание в четверг', 'расписание четверг', 
    'какие пары на четверг', 'какие пары на четверг?', 'какие пары на четверг ?', 
    'расписание на четверг?', 'расписание на четверг ?']

friday_lessons_requests = ['какие в пятницу пары','какие в пятницу пары?',
    'какие в пятницу пары ?','какие пары в пятницу','какие пары в пятницу?',
    'какие пары в пятницу ?','расписание на пятницу','пятница',
    'пары в пятницу', 'пары на пятницу', 'какое расписание в пятницу', 
    'предметы в пятницу', 'расписание в пятницу', 'предметы в пятницу?', 
    'на пятницу', 'какое расписание в пятницу', 'расписание пятница', 
    'какие пары на пятницу', 'какие пары на пятницу?', 'какие пары на пятницу ?', 
    'расписание на пятницу?', 'расписание на пятницу ?']

saturday_lessons_requests = ['какие в субботу пары','какие в субботу пары?',
    'какие в субботу пары ?','какие пары в субботу','какие пары в субботу?',
    'какие пары в субботу ?','расписание на субботу','суббота',
    'пары в субботу', 'пары на субботу', 'какое расписание в субботу', 
    'предметы в субботу', 'расписание в субботу', 'предметы в субботу?', 
    'на субботу', 'какое расписание в субботу', 'расписание суббота', 
    'какие пары на субботу', 'какие пары на субботу?', 'какие пары на субботу ?', 
    'расписание на суббту?', 'расписание на суббту ?']

today_lessons_requests = ['какие пары сегодня','какие пары сегодня?',
    'какие пары сегодня ?', 'какие сегодня пары','какие сегодня пары ?',
    'сегодня', 'какое сегодня расписание', 'расписание на сегодня', 
    'что сегодня','что сегодня?','что сегодня ?', 'на сегодня', 'сегодня',
    'сегодня?', 'сегодня ?', 'сегодня пары какие', 'пары на сегодня', 
    'какие пары', 'какие пары?', 'какие пары ?', 'какие сегодня пары?']

tomorrow_lessons_requests = ['какие пары завтра','какие пары завтра?',
    'какие пары завтра ?', 'какие завтра пары','какие завтра пары ?',
    'завтра', 'какое завтра расписание', 'расписание на завтра', 'что завтра',
    'что завтра?', 'что завтра ?', 'на завтра', 'завтра', 'завтра?',
    'завтра ?', 'завтра пары какие', 'пары на завтра', 'какие завтра пары?']

day_after_tomorrow_lessond_requests = ['какие послезавтра пары', 
    'какие послезавтра пары?', 'какие послезавтра пары ?', 
    'какие пары послезавтра', 'какие пары послезавтра?', 
    'какие пары послезавтра ?', 'послезавтра', 'какие пары после завтра?', 
    'расписание на послезавтра']

# добавить поиск по КАФЕДРАМ 

def find_message_value(text, user_id):

    if text in monday_lessons_requests:
        next_monday = next_weekday(0)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'понедельник':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "понедельник"'
            message = message + additional_text
        return message
    elif text in tuesday_lessons_requests:
        next_monday = next_weekday(1)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'вторник':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "вторник"'
            message = message + additional_text
        return message
    elif text in wednesday_lessons_requests:
        next_monday = next_weekday(2)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'среда':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "среда"'
            message = message + additional_text
        return message
    elif text in thursday_lessons_requests:
        next_monday = next_weekday(3)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'четверг':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "четверг"'
            message = message + additional_text
        return message
    elif text in friday_lessons_requests:
        next_monday = next_weekday(4)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'пятница':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "пятница"'
            message = message + additional_text
        return message
    elif text in saturday_lessons_requests:
        next_monday = next_weekday(5)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        if text != 'суббота':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "суббота"'
            message = message + additional_text
        return message
    elif text in today_lessons_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        message = find_lessons_at_date.return_lessons_at_date(user_id, time_now)
        if text != 'сегодня':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "сегодня"'
        return message
    elif text in tomorrow_lessons_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        tomorrow = time_now + datetime.timedelta(days=1)
        message = find_lessons_at_date.return_lessons_at_date(user_id, tomorrow)
        if text != 'завтра':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "завтра"'
        return message
    elif text in day_after_tomorrow_lessond_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        after_tomorrow = time_now + datetime.timedelta(days=2)
        message = find_lessons_at_date.return_lessons_at_date(user_id, after_tomorrow)
        if text != 'послезавтра':
            additional_text = '\nВместо длинного запроса ты можешь писать просто "послезавтра"'
        return message
    else:
        return False
    
