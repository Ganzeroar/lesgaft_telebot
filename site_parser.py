import requests
import datetime
import pytz
import logging
from bs4 import BeautifulSoup

import db_functions_for_site_parser as db 
import parser

def parse_and_searching_changes():

    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")

    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))

    activate_parser = False

    course_names = ['lovs_1_kurs','zovs_1_kurs','lovs_2_kurs','zovs_2_kurs',
        'lovs_3_kurs','zovs_3_kurs','lovs_4_kurs','zovs_4_kurs']

    for x in range(8):
        number_of_row = x + 2
        if number_of_row % 2 == 0:
            even_or_odd = 'even'
        else:
            even_or_odd = 'odd'

        name_of_course = course_names[x]
        current_file_link = db.get_current_link(name_of_course)

        element = soup.find_all('div', class_ = f'views-row views-row-{number_of_row} views-row-{even_or_odd}')
        element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
        new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        if current_file_link == False:
            print('первый запуск')
            # Для первого запуска
            activate_parser = True

            excel_file = open(f'{name_of_course}.xlsx', 'wb')
            resp = requests.get(new_file_link)
            excel_file.write(resp.content)
            excel_file.close()

            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.insert_link_to_current_links(name_of_course, str(new_file_link))
            log_text = f'Отсутствие текущей ссылки у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link == new_file_link:
            print('одинаковые ссылки')
            log_text = f'Текущая и полученная ссылки одинаковы у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)
        elif current_file_link != new_file_link:
            print(f'различные ссылки новая ссылка: {new_file_link} и новое имя: {name_of_course}')
            activate_parser = True

            log_text = f'Полученная ссылка {new_file_link} отлична от текущей {current_file_link} у {name_of_course} в {date_and_time_now}'
            logging.info(log_text)

            excel_file = open(f'{name_of_course}.xlsx', 'wb')
            resp = requests.get(new_file_link)
            excel_file.write(resp.content)
            excel_file.close()

            db.insert_link_to_all_links(f'{name_of_course}', str(new_file_link), date_and_time_now)
            db.change_link_in_current_links(f'{name_of_course}', str(new_file_link))
    if activate_parser:
        print('парсер запущен')
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        parser.pars_files_create_dbfiles()

if __name__ == "__main__":
    parse_and_searching_changes()



















