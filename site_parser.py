import requests
import datetime
import pytz
import logging
from bs4 import BeautifulSoup

import db_functions_for_site_parser
import parser

def parse_and_download_files():
    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    element = soup.find_all('div', class_ = 'views-row views-row-2 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/1_kurs_lovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-3 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/1_kurs_zovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-4 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/2_kurs_lovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-5 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/2_kurs_zovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-6 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/3_kurs_lovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-7 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/3_kurs_zovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-8 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/4_kurs_lovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

    element = soup.find_all('div', class_ = 'views-row views-row-9 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link = element_2[0].find_all('a', href=True)[0]['href']

    f = open('/home/ganzeroar/Python/my_progs/lesgaft_telebot/4_kurs_zovs.xlsx', 'wb')
    url = file_link
    req = requests.get(url)
    f.write(req.content)
    f.close()

def parse_and_searching_changes():

    logging.basicConfig(filename="parsing_info.log", level=logging.INFO)

    url = 'http://www.lesgaft.spb.ru/ru/schedule'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")

    msc_timezone = pytz.timezone('Europe/Moscow')
    date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))

    activate_parser = False

    current_file_link_lovs_1 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('lovs_1_kurs')
    current_file_link_zovs_1 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('zovs_1_kurs')
    current_file_link_lovs_2 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('lovs_2_kurs')
    current_file_link_zovs_2 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('zovs_2_kurs')
    current_file_link_lovs_3 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('lovs_3_kurs')
    current_file_link_zovs_3 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('zovs_3_kurs')
    current_file_link_lovs_4 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('lovs_4_kurs')
    current_file_link_zovs_4 = db_functions_for_site_parser.get_current_link_of_course_and_faculty('zovs_4_kurs')

    element = soup.find_all('div', class_ = 'views-row views-row-2 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_lovs_1 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_lovs_1 == False:
        # Для первого запуска
        activate_parser = True

        excel_file = open('lovs_1_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_1)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_1_kurs', str(file_link_lovs_1), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('lovs_1_kurs', str(file_link_lovs_1))
        log_text = f'Отсутствие текущей ссылки у lovs_1 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_1 == file_link_lovs_1:
        log_text = f'Текущая и полученная ссылки одинаковы у lovs_1 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_1 != file_link_lovs_1:
        activate_parser = True

        excel_file = open('lovs_1_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_1)
        excel_file.write(resp.content)
        excel_file.close()
        
        db_functions_for_site_parser.insert_link_to_all_links('lovs_1_kurs', str(file_link_lovs_1), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('lovs_1_kurs', str(file_link_lovs_1))
        
        log_text = f'Полученная ссылка отлична от текущей у lovs_1 в {date_and_time_now}'
        logging.info(log_text)
    element = soup.find_all('div', class_ = 'views-row views-row-3 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_zovs_1 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_zovs_1 == False:
        
        excel_file = open('zovs_1_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_1)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_1_kurs', str(file_link_zovs_1), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('zovs_1_kurs', str(file_link_zovs_1))
        log_text = f'Отсутствие текущей ссылки у zovs_1 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_1 == file_link_zovs_1:
        log_text = f'Текущая и полученная ссылки одинаковы у zovs_1 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_1 != file_link_zovs_1:
        activate_parser = True

        excel_file = open('zovs_1_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_1)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_1_kurs', str(file_link_zovs_1), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('zovs_1_kurs', str(file_link_zovs_1))
        
        log_text = f'Полученная ссылка отлична от текущей у zovs_1 в {date_and_time_now}'
        logging.info(log_text)

    element = soup.find_all('div', class_ = 'views-row views-row-4 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_lovs_2 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_lovs_2 == False:

        excel_file = open('lovs_2_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_2)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_2_kurs', str(file_link_lovs_2), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('lovs_2_kurs', str(file_link_lovs_2))
        log_text = f'Отсутствие текущей ссылки у lovs_2 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_2 == file_link_lovs_2:
        log_text = f'Текущая и полученная ссылки одинаковы у lovs_2 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_2 != file_link_lovs_2:
        activate_parser = True

        excel_file = open('lovs_2_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_2)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_2_kurs', str(file_link_lovs_2), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('lovs_2_kurs', str(file_link_lovs_2))
        
        log_text = f'Полученная ссылка отлична от текущей у lovs_2 в {date_and_time_now}'
        logging.info(log_text)


    element = soup.find_all('div', class_ = 'views-row views-row-5 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_zovs_2 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_zovs_2 == False:

        excel_file = open('zovs_2_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_2)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_2_kurs', str(file_link_zovs_2), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('zovs_2_kurs', str(file_link_zovs_2))
        log_text = f'Отсутствие текущей ссылки у zovs_2 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_2 == file_link_zovs_2:
        log_text = f'Текущая и полученная ссылки одинаковы у zovs_2 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_2 != file_link_zovs_2:
        activate_parser = True

        excel_file = open('zovs_2_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_2)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_2_kurs', str(file_link_zovs_2), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('zovs_2_kurs', str(file_link_zovs_2))
        
        log_text = f'Полученная ссылка отлична от текущей у zovs_2 в {date_and_time_now}'
        logging.info(log_text)

    element = soup.find_all('div', class_ = 'views-row views-row-6 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_lovs_3 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_lovs_3 == False:

        excel_file = open('lovs_3_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_3)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_3_kurs', str(file_link_lovs_3), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('lovs_3_kurs', str(file_link_lovs_3))
        log_text = f'Отсутствие текущей ссылки у lovs_3 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_3 == file_link_lovs_3:
        log_text = f'Текущая и полученная ссылки одинаковы у lovs_3 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_3 != file_link_lovs_3:
        activate_parser = True

        excel_file = open('lovs_3_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_3)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_3_kurs', str(file_link_lovs_3), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('lovs_3_kurs', str(file_link_lovs_3))
        
        log_text = f'Полученная ссылка отлична от текущей у lovs_3 в {date_and_time_now}'
        logging.info(log_text)

    element = soup.find_all('div', class_ = 'views-row views-row-7 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_zovs_3 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_zovs_3 == False:

        excel_file = open('zovs_3_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_3)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_3_kurs', str(file_link_zovs_3), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('zovs_3_kurs', str(file_link_zovs_3))
        log_text = f'Отсутствие текущей ссылки у zovs_3 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_3 == file_link_zovs_3:
        log_text = f'Текущая и полученная ссылки одинаковы у zovs_3 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_3 != file_link_zovs_3:
        activate_parser = True

        excel_file = open('zovs_3_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_3)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_3_kurs', str(file_link_zovs_3), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('zovs_3_kurs', str(file_link_zovs_3))
        
        log_text = f'Полученная ссылка отлична от текущей у zovs_3 в {date_and_time_now}'
        logging.info(log_text)

    element = soup.find_all('div', class_ = 'views-row views-row-8 views-row-even')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_lovs_4 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_lovs_4 == False:

        excel_file = open('lovs_4_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_4)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_4_kurs', str(file_link_lovs_4), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('lovs_4_kurs', str(file_link_lovs_4))
        log_text = f'Отсутствие текущей ссылки у lovs_4 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_4 == file_link_lovs_4:
        log_text = f'Текущая и полученная ссылки одинаковы у lovs_4 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_lovs_4 != file_link_lovs_4:
        activate_parser = True

        excel_file = open('lovs_4_kurs.xlsx', 'wb')
        resp = requests.get(file_link_lovs_4)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('lovs_4_kurs', str(file_link_lovs_4), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('lovs_4_kurs', str(file_link_lovs_4))
        
        log_text = f'Полученная ссылка отлична от текущей у lovs_4 в {date_and_time_now}'
        logging.info(log_text)

    element = soup.find_all('div', class_ = 'views-row views-row-9 views-row-odd')
    element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
    file_link_zovs_4 = element_2[0].find_all('a', href=True)[0]['href']
    if current_file_link_zovs_4 == False:

        excel_file = open('zovs_4_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_4)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_4_kurs', str(file_link_zovs_4), date_and_time_now)
        db_functions_for_site_parser.insert_link_to_current_links('zovs_4_kurs', str(file_link_zovs_4))
        log_text = f'Отсутствие текущей ссылки у zovs_1 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_4 == file_link_zovs_4:
        log_text = f'Текущая и полученная ссылки одинаковы у zovs_4 в {date_and_time_now}'
        logging.info(log_text)
    elif current_file_link_zovs_4 != file_link_zovs_4:
        activate_parser = True

        excel_file = open('time_tables/zovs_4_kurs.xlsx', 'wb')
        resp = requests.get(file_link_zovs_4)
        excel_file.write(resp.content)
        excel_file.close()

        db_functions_for_site_parser.insert_link_to_all_links('zovs_4_kurs', str(file_link_zovs_4), date_and_time_now)
        db_functions_for_site_parser.change_link_in_current_links('zovs_4_kurs', str(file_link_zovs_4))
        
        log_text = f'Полученная ссылка отлична от текущей у zovs_4 в {date_and_time_now}'
        logging.info(log_text)
    if activate_parser:
        log_text = f'Парсер файлов запущен в {date_and_time_now}'
        logging.info(log_text)
        parser.pars_files_create_dbfiles()
if __name__ == "__main__":
    parse_and_searching_changes()



















