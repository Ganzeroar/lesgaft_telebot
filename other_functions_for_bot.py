# -*- coding: utf-8 -*-

import lesgaft_bot_db
import subjects_db
import datetime
import time
import pytz
import texts_for_lesgaft_bot

def return_russian_day_of_week(eng_day):
    if eng_day == 'Mon':
        return 'понедельник'
    elif eng_day == 'Tue':
        return 'вторник'
    elif eng_day == 'Wed':
        return 'среду'
    elif eng_day == 'Thu':
        return 'четеверг'
    elif eng_day == 'Fri':
        return 'пятницу'
    elif eng_day == 'Sat':
        return 'субботу'
    elif eng_day == 'Sun':
        return 'воскресенье'
    
def is_time_between(begin_time, end_time, check_time=None):
    msc_timezone = pytz.timezone('Europe/Moscow')

    check_time = check_time or datetime.datetime.now(tz=msc_timezone).time()
    #check_time = datetime.time(10,10)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def return_message_text_about_current_lesson(user_id, number_of_lesson):
    msc_timezone = pytz.timezone('Europe/Moscow')
    
    try:
        number_of_group = lesgaft_bot_db.get_group_number(user_id)[0][0]
    except:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    else:
        #d = datetime.date(2019, 11, 18)
        #t = datetime.time(10, 10)
        #date_and_time_now =  datetime.datetime.combine(d, t)
        date_and_time_now = datetime.datetime.now(tz=msc_timezone)
        today_date = str(date_and_time_now.day) + '.' + str(date_and_time_now.month) + '.'
        today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
        if bool(today_subjects) == False or today_subjects[number_of_lesson][0] == None:
            return texts_for_lesgaft_bot.error
        else:
            list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
        try:
            if today_subjects[number_of_lesson][0] != 'Нет предмета':
                current_subject = today_subjects[number_of_lesson][0]
                text = f'Сейчас у вас {current_subject}'
                return text
            if today_subjects[number_of_lesson][0] == 'Нет предмета':
                return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        except Exception as exception:
            print('error ' + str(exception))
    
def return_message_text_to_about_time_before_lesson(user_id, number_of_lesson):
    msc_timezone = pytz.timezone('Europe/Moscow')

    try:
        number_of_group = lesgaft_bot_db.get_group_number(user_id)[0][0]
    except:
        return 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.'
    name_of_group = 'Группа_' + str(number_of_group)
    db_name = subjects_db.get_db_name(number_of_group)
    if db_name == None:
        return 'Твоей группы не существует. Измени номер группы.'
    else:
        #d = datetime.date(2019, 11, 21)
        #t = datetime.time(6, 0)
        #date_and_time_now =  datetime.datetime.combine(d, t)
        date_and_time_now = datetime.datetime.now(tz=msc_timezone)
        today_date = str(date_and_time_now.day) + '.' + str(date_and_time_now.month) + '.'
        today_subjects = subjects_db.get_subjects_today(name_of_group, db_name, today_date)
        if number_of_lesson >= 5:
            return 'Сегодня у тебя больше нет пар.' 
        if bool(today_subjects) == False or today_subjects[number_of_lesson][0] == None:
            return texts_for_lesgaft_bot.error
        else:
            list_of_times = ['9:45', '11:30', '13:30', '15:15', '17:00']
        try:
            if today_subjects[number_of_lesson][0] != 'Нет предмета':
                next_subject = today_subjects[number_of_lesson][0]
                formate_of_time = '%H:%M' 
                today_time = date_and_time_now.strftime("%H:%M")
                today_date = datetime.datetime.strptime(today_time, formate_of_time)
                next_start_time = datetime.datetime.strptime(list_of_times[number_of_lesson], formate_of_time)
                time_to_lesson = str(next_start_time - today_date)[0:4]
                class_location = find_class_location(next_subject)
                text = f'Через {time_to_lesson} начнётся {next_subject}, {class_location}' # вот тут добавить где 
                return text
            if today_subjects[number_of_lesson][0] == 'Нет предмета':
                return return_message_text_to_about_time_before_lesson(user_id, number_of_lesson + 1)
        except Exception as exception:
            print('error ' + str(exception))



def find_class_location_used_number(number_of_class):
    dict_of_all_classes = {
        '1' : ' Мойка, третий этаж, от лестницы налево', 
        '2' : ' Мойка, третий этаж, от лестницы налево',
        '3' : ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '6' : ' Справа за аркой, что справа от входа в Мойку, который на территории университета',
        '9' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '14' : ' Мойка, третий этаж, от лестницы направо, по правую сторону',
        '17' : ' Мойка, второй этаж, налево от охранника, по правую сторону',
        '18' : ' Мойка, второй этаж, налево от охранника, по правую сторону',
        '19' : ' Мойка, второй этаж, налево от охранника, по правую сторону',
        '20' : ' Мойка, второй этаж, налево от охранника, по правую сторону',
        '21' : ' Мойка, второй этаж, налево от охранника, по правую сторону', 
        '26' : ' Мойка, второй этаж, налево от охранника, по левую сторону',
        '28' : ' Мойка, второй этаж, налево от охранника, по левую сторону',
        '33' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '34' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '35' :  'Мойка, второй этаж, направо от охранника, по правую сторону',
        '36' :  'Мойка, второй этаж, направо от охранника, по правую сторону',
        '39' :  'Мойка, второй этаж, направо от охранника, по правую сторону',
        '40' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '42' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '43' : ' Мойка, второй этаж, направо от охранника, по правую сторону',
        '44' : ' Мойка, второй этаж, направо от охранника, по правую сторону',
        '45' : ' Мойка, второй этаж, направо от охранника, по правую сторону',
        '46' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '54' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '55' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '64' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '71' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '72' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '73' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '78' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '79' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '80' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '81' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, по правую сторону',
        '82' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону',
        '83' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону',
        '85' : ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево',
        '86' : ' Мойка, второй этаж, после угловой лестницы прямо и налево',
        '87' : ' Мойка, второй этаж, после угловой лестницы прямо',
        '88' : ' Мойка, второй этаж, после угловой лестницы прямо и направо',
        '89' : ' Мойка, второй этаж, после угловой лестницы направо',
        '90' : ' Мойка, второй этаж, после угловой лестницы слева',
        '93' : ' Мойка, первый этаж, после входа направо',
        '94' : ' Мойка, первый этаж, после входа направо',
        '96' : ' Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '97' : ' Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '98' : ' Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '99' : ' Мойка, первый этаж, после входа направо и налево',
        '104' : ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '105' : ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '119' : ' Мойка, первый этаж, после входа налево, направо, направо',
        '121' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '122' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '123' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '124' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '125' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '126' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '127' : ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '128' : ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '129' : ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '131' : ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '132' : ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '135' : ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '150' : ' Мойка, справа от спуска к выходу от охранника на втором этаже',
        '223' : ' Мойка, второй этаж, направо от охранника, по левую сторону',
        '233' : ' Мойка, третий этаж, сразу после лестницы',
        '303' : ' Главный корпус, второй этаж, от маленькой лестницы направо',
        '304' : ' Главный корпус, второй этаж, от маленькой лестницы прямо',
        '305' : ' Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону',
        '306' : ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '307' : ' Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону',
        '308' : ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '310' : ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '312' : ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, прямо',
        '313' : ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '315' : ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '317' : ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '321' : ' Главный корпус, второй этаж, от главной лестницы налево',
        '322' : ' Главный корпус, второй этаж, от главной лестницы прямо',
        '323' : ' Главный корпус, второй этаж, от главной лестницы направо',
        '401' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '402' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '403' : ' Главный корпус, третий этаж, после лестницы направо, направо и прямо',
        '404' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '405' : ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '407' : ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '409' : ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '410' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '411' : ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '412' : ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '413' : ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '414' : ' Главный корпус, третий этаж, после лестницы направо и прямо',
        '416' : ' Главный корпус, третий этаж, после лестницы налево прямо',
        '418' : ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону',
        '419' : ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '421' : ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '422' : ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону',
        '423' : ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '426' : ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону'
    }   
    try:
        text = dict_of_all_classes[number_of_class]
        return text
    except:
        return 'Такой аудитории я не знаю'

def find_class_location(subject):  
    
    if 'ауд.' in subject:
        if '1' in subject:
            if '10' in subject:
                if '104' in subject and len(subject) == 3:
                    return ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо'
                elif '105' in subject and len(subject) == 3:
                    return ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо'
            elif '11' in subject:
                if '119' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, направо'
            elif '12' in subject:
                if '121' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '122' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '123' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '124' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '125' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '126' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '127' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по правую сторону'
                elif '128' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону'
                elif '129' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону'
            elif '13' in subject:
                if '131' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону'
                elif '132' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону'
                elif '135' in subject and len(subject) == 3:
                    return ' Мойка, первый этаж, после входа налево, направо, налево, по левую сторону'
            elif '15' in subject:
                if '150' in subject and len(subject) == 3:
                    return ' Мойка, справа от спуска к выходу от охранника на втором этаже'
            if '14' in subject and len(subject) == 2:
                return ' Мойка, третий этаж, от лестницы направо, по правую сторону'
            elif '17' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по правую сторону'
            elif '18' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по правую сторону'
            elif '19' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по правую сторону'
            elif len(subject) == 1:
                return ' Мойка, третий этаж, от лестницы налево'
        elif '2' in subject:
            if '20' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по правую сторону'
            elif '21' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по правую сторону'
            elif '22' in subject:
                if '223' in subject and len(subject) == 3:
                    return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif '23' in subject:
                if '233' in subject and len(subject) == 3:
                    return ' Мойка, третий этаж, сразу после лестницы'
            elif '26' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по левую сторону'
            elif '28' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, налево от охранника, по левую сторону'
            elif len(subject) == 1:
                return ' Мойка, третий этаж, от лестницы налево'
        elif '3' in subject:
            if '30' in subject:
                if '303' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы направо'
                elif '304' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы прямо'
                elif '305' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону'
                elif '306' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону'
                elif '307' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону'
                elif '308' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону'
            elif '31' in subject:
                if '310' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону'
                elif '312' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, прямо'
                elif '313' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне'
                elif '315' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне'
                elif '317' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне'
            elif '32' in subject:
                if '321' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от главной лестницы налево'
                elif '322' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от главной лестницы прямо'
                elif '323' in subject and len(subject) == 3:
                    return ' Главный корпус, второй этаж, от главной лестницы направо'

            elif '33' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif '34' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif '35' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif '36' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif '39' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif len(subject) == 1:
                return ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо'

        elif '4' in subject:
            if '40' in subject:
                if '401' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
                elif '402' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
                elif '403' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо, направо и прямо'
                elif '404' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
                elif '405' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону'
                elif '407' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону'
                elif '409' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону'
                elif len(subject) == 2:
                    return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif '41' in subject:
                if '410' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
                elif '411' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону'
                elif '412' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
                elif '413' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону'
                elif '414' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы направо и прямо'
                elif '416' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево прямо'
                elif '418' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону'
                elif '419' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону'
            elif '42' in subject:
                if '421' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону'
                elif '422' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону'
                elif '423' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону'
                elif '426' in subject and len(subject) == 3:
                    return ' Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону'
                elif len(subject) == 2:
                    return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif '43' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif '44' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif '45' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по правую сторону'
            elif '46' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, направо от охранника, по левую сторону'
            elif len(subject) == 2:
                return ' Мойка, третий этаж, от лестницы направо, по левую сторону'

        elif '5' in subject:
            if '54' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца'
            elif '55' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца'

        elif '6' in subject:
            if '64' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца'
            elif len(subject) == 2:
                return ' Справа за аркой, что справа от входа в Мойку, который на территории университета'
        elif '7' in subject:
            if '71' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону'
            elif '72' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону'
            elif '73' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону'
            elif '78' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца'
            elif '79' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца'

        elif '8' in subject:
            if '80' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца'
            elif '81' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, по правую сторону'
            elif '82' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону'
            elif '83' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону'
            elif '85' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо, налево, налево'
            elif '86' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо и налево'
            elif '87' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо'
            elif '88' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы прямо и направо'
            elif '89' in subject  and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы направо'

        elif '9' in subject:
            if '90' in subject and len(subject) == 2:
                return ' Мойка, второй этаж, после угловой лестницы слева'
            elif '93' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо'
            elif '94' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо'
            elif '96' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе'
            elif '97' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо, налево и направо, по левую сторону'
            elif '98' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо, налево и направо, по левую сторону'
            elif '99' in subject and len(subject) == 2:
                return ' Мойка, первый этаж, после входа направо и налево'
            else:
                return ' Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону'
    elif 'Зал' in subject:
        if '№2' in subject:
            return ' Манеж, первый этаж'
        elif '№3' in subject:
            return ' Манеж, третий этаж'
        elif '№5' in subject:
            return ' '
    elif 'Мойка' in subject:
        if 'к.2' in subject:
            if 'ауд. 7' in subject:
                return ' Вход со стороны стадиона, второй этаж'
            elif 'ауд. 8' in subject:
                return ' Вход со стороны стадиона, второй этаж'
            elif 'ауд. 9' in subject:
                return ' Вход со стороны стадиона, второй этаж'
    elif 'Кафедра' in subject:
        if 'ТиМФОР' in subject:
            return ' '
        elif 'ТиМИВС' in subject:
            return ' '
        elif 'ПСС' in subject:
            return ' '
        elif 'Элективные дисциплины' in subject:
            return ' '
        elif 'Педагогики' in subject:
            return ' Мойка, третий этаж, от лестницы направо'
    elif 'Каф.' in subject:
        if 'проф.мед.' in subject:
            return ' Главный корпус, маленькая лестница с выходом к Ленину, второй этаж'
        elif 'анатомии' in subject:
            return ' Главный корпус, по лестнице с клеткой на втором этаже вниз, затем направо'
        elif 'ин.языков' in subject:
            return ' '
    elif 'Бассейн' in subject:
        return ' '
    elif 'Манеж' in subject:
        return ' '
    elif 'Кавголово' in subject:
        return ' '
            