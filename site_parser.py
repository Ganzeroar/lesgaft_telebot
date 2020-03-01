
import requests
import datetime
import pytz
import logging
from bs4 import BeautifulSoup

import db_funcs_for_site_parser as db 
import excel_parser

class Site_parser():

    def is_Changed(self, new_file_link):
        name_of_course = self.get_name_of_course(new_file_link)
        current_file_link = db.get_current_link(name_of_course)
        if current_file_link != new_file_link:
            return True
        else:
            return False

    def get_date_and_time_now(self):
        msc_timezone = pytz.timezone('Europe/Moscow')
        date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
        return date_and_time_now

    def create_new_excel_files(self, route, changed_files):
        for new_file_link in changed_files:
            date_and_time_now = self.get_date_and_time_now()
            name_of_course = self.get_name_of_course(new_file_link)
            self.create_table(route, name_of_course, new_file_link)
            db.insert_link_to_all_links(name_of_course, str(new_file_link), date_and_time_now)
            db.insert_link_to_current_links(name_of_course, str(new_file_link))
    
    def create_table(self, route, name_of_course, new_file_link):
        excel_file = open(f'time_tables/{route}/{name_of_course}.xlsx', 'wb')
        resp = requests.get(new_file_link)
        excel_file.write(resp.content)
        excel_file.close()

    def get_soup_obj(self):
        url = 'http://www.lesgaft.spb.ru/ru/schedule'
        resp = requests.get(url)
        soup_obj = BeautifulSoup(resp.text, "lxml")
        return soup_obj


class Site_parser_undergraduate(Site_parser):

    def run_full_time_undergraduate_parser(self):
        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            print('Изменения в ' + str(changed_files))
            self.create_new_excel_files('full_time_undergraduate', changed_files)
            self.run_excel_parser(changed_files)

    def find_changed_files(self):
        changed_files = []

        for number in range(8):
            # необходимо что бы правильно определить HTML код нужного расписания
            # ввиду плохого нейминга элементов на сайте
            number_of_row = number + 2
            
            new_file_link = self.get_file_link_from_site_full_time_undergraduate(number_of_row)
            if self.is_Changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def get_file_link_from_site_full_time_undergraduate(self, number_of_row):
        new_file_link = self.find_file_link(number_of_row)
        return new_file_link

    def find_file_link(self, number_of_row):
        soup_obj = self.get_soup_obj()
        html_string = self.create_html_string(number_of_row)
        element = soup_obj.find_all('div', class_ = html_string)
        element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
        new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def create_html_string(self, number_of_row):
        even_or_odd = self.return_even_or_odd(number_of_row)
        html_string = f'views-row views-row-{number_of_row} views-row-{even_or_odd}'
        return html_string

    def return_even_or_odd(self, number_of_row):
        if number_of_row % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def get_name_of_course(self, file_link):
        course_names = ['1_kurs_lovs','1_kurs_zovs','2_kurs_lovs','2_kurs_zovs',
            '3_kurs_lovs','3_kurs_zovs','4_kurs_lovs','4_kurs_zovs']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        first_part = name[:6]
        second_part = name[-4:]
        name_of_course = second_part + '_' + first_part
        return name_of_course

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser()
            parser.parse_work_file_using_name(name_of_course, 'full_time_undergraduate')

class Site_parser_undergraduate_imist(Site_parser):
    
    def run_full_time_undergraduate_imist_parser(self):
        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files('full_time_undergraduate/imst', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_links_from_site_imist(self):
        soup_obj = self.get_soup_obj()
        element = soup_obj.find_all('div', class_ = f'views-row views-row-10 views-row-even')
        element_2 = element[0].find_all('div', class_ = 'field field-name-field-fl1 field-type-file field-label-hidden')
        imist_1 = element_2[0].find_all('a', href=True)[0]['href']
        imist_2 = element_2[0].find_all('a', href=True)[1]['href']
        imist_3 = element_2[0].find_all('a', href=True)[2]['href']
        imist_4 = element_2[0].find_all('a', href=True)[3]['href']

        return imist_1, imist_2, imist_3, imist_4

    def find_changed_files(self):
        changed_files = []
        links_from_site = self.return_file_links_from_site_imist()

        for number in range(4):
            new_file_link = links_from_site[number]
            if self.is_Changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def get_name_of_course(self, file_link):
        course_names = ['1_kurs_imst', '2_kurs_imst', '3_kurs_imst', '4_kurs_imst']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        first_part = name[:6]
        second_part = name[-4:]
        name_of_course = second_part + '_' + first_part
        return name_of_course

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser()
            parser.parse_work_file_using_name(name_of_course, 'full_time_undergraduate/imst')



class Site_parser_magistracy_fk(Site_parser):

    def run_full_time_magistracy_fk(self):

        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files('full_time_magistracy_fk', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_fk(self, number_of_course):
        soup_obj = self.get_soup_obj()
        element = soup_obj.find_all('div', class_ = f'views-row views-row-11 views-row-odd')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_ = 'field-item even')
            new_file_link = element_2[2].find_all('a', href=True)[0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_ = 'field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link
    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_fk(number)
            print(new_file_link)
            if self.is_Changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def get_name_of_course(self, file_link):
        course_names = ['mag_1_kurs_fk_sport_ppo', 'mag_2_kurs_fk_sport_ppo']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        if 'mag_1_kurs_fk_sport_ppo' in name:
            return 'magistracy_fk_full_time_1_kurs'
        elif 'mag_2_kurs_fk_sport_ppo' in name:
            return 'magistracy_fk_full_time_2_kurs'

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser()
            parser.parse_work_file_using_name(name_of_course, 'full_time_magistracy_fk')

class Site_parser_magistracy_afk(Site_parser):

    def run_full_time_magistracy_afk(self):

        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files('full_time_magistracy_afk', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_afk(self, number_of_course):
        soup_obj = self.get_soup_obj()
        element = soup_obj.find_all('div', class_ = f'views-row views-row-12 views-row-even')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_ = 'field-item even')
            new_file_link = element_2[1].find_all('a', href=True)[0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_ = 'field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_afk(number)
            print(new_file_link)
            if self.is_Changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def get_name_of_course(self, file_link):
        course_names = ['mag_1_kurs_afk', 'mag_2_kurs_afk']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        if 'mag_1_kurs_afk' in name:
            return 'magistracy_afk_full_time_1_kurs'
        elif 'mag_2_kurs_afk' in name:
            return 'magistracy_afk_full_time_2_kurs'

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser()
            parser.parse_work_file_using_name(name_of_course, 'full_time_magistracy_afk')


class Site_parser_magistracy_imst(Site_parser):
    
    def run_full_time_magistracy_imst(self):
        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files('full_time_magistracy_imst', changed_files)
            print(123)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_imst(self, number_of_course):
        soup_obj = self.get_soup_obj()
        element = soup_obj.find_all('div', class_ = f'views-row views-row-13 views-row-odd')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_ = 'field-item even')
            new_file_link = element_2[1].find_all('a', href=True)[0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_ = 'field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_imst(number)
            print(new_file_link)
            if self.is_Changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def get_name_of_course(self, file_link):
        course_names = ['mag_1_kurs_imst', 'mag_2_kurs_imst']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        if 'mag_1_kurs_imst' in name:
            return 'magistracy_imst_full_time_1_kurs'
        elif 'mag_2_kurs_imst' in name:
            return 'magistracy_imst_full_time_2_kurs'

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser()
            parser.parse_work_file_using_name(name_of_course, 'full_time_magistracy_fk')


def run_all_parsers():
    parser_1 = Site_parser_undergraduate()
    parser_1.run_full_time_undergraduate_parser()
    parser_2 = Site_parser_undergraduate_imist()
    parser_2.run_full_time_undergraduate_imist_parser()
    parser_3 = Site_parser_magistracy_fk()
    parser_3.run_full_time_magistracy_fk()
    parser_4 = Site_parser_magistracy_afk()
    parser_4.run_full_time_magistracy_afk()
    parser_5 = Site_parser_magistracy_imst()
    parser_5.run_full_time_magistracy_imst()


if __name__ == "__main__":
    run_all_parsers()