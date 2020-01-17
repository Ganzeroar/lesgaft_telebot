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
    'пары в понедельник', 'пары на понедельник']

tuesday_lessons_requests = ['какие во вторник пары','какие во вторник пары?',
    'какие во вторник пары ?','какие пары во вторник','какие пары во вторник?',
    'какие пары во вторник ?','расписание на вторник','вторник',
    'пары во вторник', 'пары на вторник']

wednesday_lessons_requests = ['какие в среду пары','какие в среду пары?',
    'какие в среду пары ?','какие пары в среду','какие пары в среду?',
    'какие пары в среду ?','расписание на среду','среда','пары в среду', 
    'пары на среду']

thursday_lessons_requests = ['какие в четверг пары','какие в четверг пары?',
    'какие в четверг пары ?','какие пары в четверг','какие пары в четверг?',
    'какие пары в четверг ?','расписание на четверг','четверг',
    'пары в четверг', 'пары на четверг']

friday_lessons_requests = ['какие в пятницу пары','какие в пятницу пары?',
    'какие в пятницу пары ?','какие пары в пятницу','какие пары в пятницу?',
    'какие пары в пятницу ?','расписание на пятницу','пятница',
    'пары в пятницу', 'пары на пятницу']

saturday_lessons_requests = ['какие в субботу пары','какие в субботу пары?',
    'какие в субботу пары ?','какие пары в субботу','какие пары в субботу?',
    'какие пары в субботу ?','расписание на субботу','суббота',
    'пары в субботу', 'пары на субботу']

today_lessons_requests = ['какие пары сегодня','какие пары сегодня?',
    'какие пары сегодня ?', 'какие сегодня пары','какие сегодня пары ?',
    'сегодня', 'какое сегодня расписание', 'расписание на сегодня', 
    'что сегодня','что сегодня?','что сегодня ?', 'на сегодня', 'сегодня',
    'сегодня?', 'сегодня ?']

tomorrow_lessons_requests = ['какие пары завтра','какие пары завтра?',
    'какие пары завтра ?', 'какие завтра пары','какие завтра пары ?',
    'завтра', 'какое завтра расписание', 'расписание на завтра', 'что завтра',
    'что завтра?', 'что завтра ?', 'на завтра', 'завтра', 'завтра?',
    'завтра ?']

day_after_tomorrow_lessond_requests = ['какие послезавтра пары', 
    'какие послезавтра пары?', 'какие послезавтра пары ?', 
    'какие пары послезавтра', 'какие пары послезавтра?', 
    'какие пары послезавтра ?', 'послезавтра']

# добавить поиск по КАФЕДРАМ 

def find_message_value(text, user_id):

    if text in monday_lessons_requests:
        next_monday = next_weekday(0)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in tuesday_lessons_requests:
        next_monday = next_weekday(1)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in wednesday_lessons_requests:
        next_monday = next_weekday(2)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in thursday_lessons_requests:
        next_monday = next_weekday(3)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in friday_lessons_requests:
        next_monday = next_weekday(4)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in saturday_lessons_requests:
        next_monday = next_weekday(5)
        message = find_lessons_at_date.return_lessons_at_date(user_id, next_monday)
        return message
    elif text in today_lessons_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        message = find_lessons_at_date.return_lessons_at_date(user_id, time_now)
        return message
    elif text in tomorrow_lessons_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        tomorrow = time_now + datetime.timedelta(days=1)
        message = find_lessons_at_date.return_lessons_at_date(user_id, tomorrow)
        return message
    elif text in day_after_tomorrow_lessond_requests:
        time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
        after_tomorrow = time_now + datetime.timedelta(days=2)
        message = find_lessons_at_date.return_lessons_at_date(user_id, after_tomorrow)
        return message
    else:
        return False
    
