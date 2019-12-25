# -*- coding: utf-8 -*-

import datetime
import pytz
import find_lessons_at_date
import texts_for_lesgaft_bot

def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return date + datetime.timedelta(days_ahead)

msc_timezone = pytz.timezone('Europe/Moscow')
date_and_time_now = datetime.datetime.now(tz=msc_timezone)

day = date_and_time_now.day
mounh = date_and_time_now.month
year = date_and_time_now.year
date = datetime.date(year, mounh, day)

next_monday = next_weekday(date, 0)
print(next_monday) # 2019-12-23

monday_lessons_requests = ['какие в понедельник пары','какие в понедельник пары?',
    'какие в понедельник пары ?','какие пары в понедельник','какие пары в понедельник?',
    'какие пары в понедельник ?','расписание на понедельник','понедельник',]

tuesday_lessons_requests = ['какие в вторник пары','какие в вторник пары?',
    'какие в вторник пары ?','какие пары в вторник','какие пары в вторник?',
    'какие пары в вторник ?','расписание на вторник','вторник',]

wednesday_lessons_requests = ['какие в среду пары','какие в среду пары?',
    'какие в среду пары ?','какие пары в среду','какие пары в среду?',
    'какие пары в среду ?','расписание на среду','среда',]

thursday_lessons_requests = ['какие в четверг пары','какие в четверг пары?',
    'какие в четверг пары ?','какие пары в четверг','какие пары в четверг?',
    'какие пары в четверг ?','расписание на четверг','четверг',]

friday_lessons_requests = ['какие в пятницу пары','какие в пятницу пары?',
    'какие в пятницу пары ?','какие пары в пятницу','какие пары в пятницу?',
    'какие пары в пятницу ?','расписание на пятницу','пятница',]

saturday_lessons_requests = ['какие в субботу пары','какие в субботу пары?',
    'какие в субботу пары ?','какие пары в субботу','какие пары в субботу?',
    'какие пары в субботу ?','расписание на субботу','суббота',]

tomorrow_lessons_requests = ['какие пары завтра','какие пары завтра?','какие пары завтра ?',
    'какие завтра пары','какие завтра пары ?','завтра', 'какое завтра расписание']

stupid_requests = ['какие послезавтра пары','что сегодня', 'на сегодня', 'когда на учёбу']

# добавить поиск по КАФЕДРАМ 

def find_message_value(text, user_id):
    #  or message.text.lower() == 'какие пары сегодня?' or message.text.lower() == 'какие сегодня пары' or message.text.lower() == 'какие пары сегодня'
    #  or message.text.lower() == 'какие завтра пары' or message.text.lower() == 'расписание на завтра' or message.text.lower() == 'какие завтра пары ?' or message.text.lower() == 'какие пары завтра ?'
    #try:
    #    text = 123
    #    return text
    #except:
    return texts_for_lesgaft_bot.invalid_text
    
