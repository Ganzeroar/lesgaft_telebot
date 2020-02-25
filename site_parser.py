# -*- coding: utf-8 -*-


import requests
import datetime
import pytz
import logging
from bs4 import BeautifulSoup

import db_funcs_for_site_parser as db 
import excel_parser_full_time_undergraduate
import excel_parser_FT_undergraduate
import excel_parser_imist_undergraduate
import excel_parser_full_time_magistracy

def create_table(route, name_of_course, new_file_link):
    excel_file = open(f'time_tables/{route}/{name_of_course}.xlsx', 'wb')
    resp = requests.get(new_file_link)
    excel_file.write(resp.content)
    excel_file.close()

def return_file_link_from_site(number_of_row, even_or_odd):
    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    element = soup.find_all('div', class_ = f'views-row views-row-{number_of_row} views-row-{even_or_odd}')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    new_file_link = element_2[0].find_all('a', href=True)[0]['href']
    return new_file_link

def return_file_link_from_site_imist(number_of_row, even_or_odd):
    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    element = soup.find_all('div', class_ = f'views-row views-row-{number_of_row} views-row-{even_or_odd}')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    imist_1 = element_2[0].find_all('a', href=True)[0]['href']
    imist_2 = element_2[0].find_all('a', href=True)[1]['href']
    imist_3 = element_2[0].find_all('a', href=True)[2]['href']
    imist_4 = element_2[0].find_all('a', href=True)[3]['href']

    return imist_1, imist_2, imist_3, imist_4

def return_even_or_odd(number_of_row):
    if number_of_row % 2 == 0:
        return 'even'
    else:
        return 'odd'

def start_chosen_parser(num_of_parser_type):
    if num_of_parser_type == 1:
        parse_and_searching_changes_full_time_undergraduate()
    elif num_of_parser_type == 2:
        parse_and_searching_changes_full_time_imist()
    elif num_of_parser_type == 3:
        parse_and_searching_changes_full_time_magistracy_fk()
    elif num_of_parser_type == 4:
        parse_and_searching_changes_full_time_magistracy_afk()
    

def return_file_link_full_time_magistracy_fk(number_of_course):
    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    element = soup.find_all('div', class_ = f'views-row views-row-11 views-row-odd')
    if number_of_course == 0:
        element_2 = element[0].find_all('div', class_ = 'field-item even')
        new_file_link = element_2[2].find_all('a', href=True)[0]['href']
    elif number_of_course == 1:
        element_2 = element[0].find_all('div', class_ = 'field-item odd')
        new_file_link = element_2[0].find_all('a', href=True)[0]['href']
    return new_file_link

def return_file_link_full_time_magistracy_afk(number_of_course):
    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    element = soup.find_all('div', class_ = f'views-row views-row-12 views-row-even')
    if number_of_course == 0:
        element_2 = element[0].find_all('div', class_ = 'field-item even')
        new_file_link = element_2[2].find_all('a', href=True)[0]['href']
    elif number_of_course == 1:
        element_2 = element[0].find_all('div', class_ = 'field-item odd')
        new_file_link = element_2[0].find_all('a', href=True)[0]['href']
    return new_file_link


def parse_and_searching_changes_full_time_magistracy_fk():
    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
    activate_parser = False

    course_names = ['magistracy_fk_full_time_1_kurs','magistracy_fk_full_time_2_kurs']

    #new_file_link = return_file_link_full_time_magistracy_fk()
    for x in range(0,2):
        new_file_link = return_file_link_full_time_magistracy_fk(x)
        name_of_course = course_names[x]
        current_file_link = db.get_current_link(name_of_course)

        if current_file_link == False:
            print('первый запуск')
            # Для первого запуска
            activate_parser = True

            create_table('full_time_magistracy_fk', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.insert_link_to_current_links(name_of_course, str(new_file_link))
            log_text = f'Отсутствие текущей ссылки у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link == new_file_link:
            print(f'одинаковые ссылки в {date_and_time_now}')
            log_text = f'Текущая и полученная ссылки одинаковы у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link != new_file_link:
            print(f'различные ссылки новая ссылка: {new_file_link} у: {name_of_course} в {date_and_time_now}')
            activate_parser = True

            log_text = f'Полученная ссылка {new_file_link} отлична от текущей {current_file_link} у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)

            create_table('full_time_magistracy_fk', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.change_link_in_current_links(name_of_course, str(new_file_link))
    if activate_parser:
        print('парсер запущен')
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        #excel_parser_full_time_undergraduate.pars_files_create_dbfiles()

def parse_and_searching_changes_full_time_magistracy_afk():
    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
    activate_parser = False

    course_names = ['magistracy_afk_full_time_1_kurs','magistracy_afk_full_time_2_kurs']

    #    new_file_link = return_file_link_full_time_magistracy_fk()
    for x in range(0,2):
        new_file_link = return_file_link_full_time_magistracy_afk(x)
        name_of_course = course_names[x]
        current_file_link = False #db.get_current_link(name_of_course)

        if current_file_link == False:
            print('первый запуск')
            # Для первого запуска
            activate_parser = True

            create_table('full_time_magistracy_afk', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.insert_link_to_current_links(name_of_course, str(new_file_link))
            log_text = f'Отсутствие текущей ссылки у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link == new_file_link:
            print(f'одинаковые ссылки в {date_and_time_now}')
            log_text = f'Текущая и полученная ссылки одинаковы у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link != new_file_link:
            print(f'различные ссылки новая ссылка: {new_file_link} у: {name_of_course} в {date_and_time_now}')
            activate_parser = True

            log_text = f'Полученная ссылка {new_file_link} отлична от текущей {current_file_link} у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)

            create_table('full_time_magistracy_afk', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.change_link_in_current_links(name_of_course, str(new_file_link))
    if activate_parser:
        print('парсер запущен')
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        #excel_parser_full_time_undergraduate.pars_files_create_dbfiles()


def parse_and_searching_changes_full_time_imist():
    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
    activate_parser = True

    course_names = ['imist_1_kurs', 'imist_2_kurs', 'imist_3_kurs', 'imist_4_kurs']

    new_file_links = return_file_link_from_site_imist(10, 'even')
    will_be_parsed = []
    for x in range(4):
        name_of_course = course_names[x]
        # 
        current_file_link = db.get_current_link(name_of_course)
        #
        new_file_link = new_file_links[x]

        if current_file_link == False:
            print('первый запуск')
            # Для первого запуска
            activate_parser = True
            will_be_parsed.append(name_of_course)

            create_table('full_time_undergraduate/imist', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, new_file_link, date_and_time_now)
            db.insert_link_to_current_links(name_of_course, new_file_link)
            log_text = f'Отсутствие текущей ссылки у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link == new_file_link:
            print(f'одинаковые ссылки в {date_and_time_now}')
            log_text = f'Текущая и полученная ссылки одинаковы у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link != new_file_link:
            print(f'различные ссылки новая ссылка: {new_file_link} у: {name_of_course} в {date_and_time_now}')
            activate_parser = True
            will_be_parsed.append(name_of_course)

            log_text = f'Полученная ссылка {new_file_link} отлична от текущей {current_file_link} у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)

            create_table('full_time_undergraduate', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.change_link_in_current_links(name_of_course, str(new_file_link))
    if activate_parser:
        print('парсер запущен')
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        for excel_file in will_be_parsed:
            excel_parser_imist_undergraduate.parse_work_file_using_name(excel_file, 'full_time_undergraduate/imist')







def parse_and_searching_changes_full_time_undergraduate():

    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
    activate_parser = False

    course_names = ['lovs_1_kurs','zovs_1_kurs','lovs_2_kurs','zovs_2_kurs',
        'lovs_3_kurs','zovs_3_kurs','lovs_4_kurs','zovs_4_kurs']

    will_be_parsed = []

    for x in range(8):
        # необходимо что бы правильно определить HTML код нужного расписания
        # ввиду плохого нейминга элементов на сайте
        number_of_row = x + 2
        even_or_odd = return_even_or_odd(number_of_row)

        name_of_course = course_names[x]
        current_file_link = db.get_current_link(name_of_course)

        new_file_link = return_file_link_from_site(number_of_row, even_or_odd)
        if current_file_link == False:
            print('первый запуск')
            # Для первого запуска
            activate_parser = True

            create_table('full_time_undergraduate', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.insert_link_to_current_links(name_of_course, str(new_file_link))
            log_text = f'Отсутствие текущей ссылки у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link == new_file_link:
            print(f'одинаковые ссылки в {date_and_time_now}')
            log_text = f'Текущая и полученная ссылки одинаковы у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link != new_file_link:
            print(f'различные ссылки новая ссылка: {new_file_link} у: {name_of_course} в {date_and_time_now}')
            activate_parser = True
            will_be_parsed.append(name_of_course)

            log_text = f'Полученная ссылка {new_file_link} отлична от текущей {current_file_link} у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)

            create_table('full_time_undergraduate', name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.change_link_in_current_links(name_of_course, str(new_file_link))
    if activate_parser:
        print('парсер запущен')
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        for excel_file in will_be_parsed:
            excel_parser_full_time_magistracy.run_excel_parser_undergraduate()

if __name__ == "__main__":
    start_chosen_parser(4)