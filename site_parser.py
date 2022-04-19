
import requests
import datetime
import pytz
import logging
from bs4 import BeautifulSoup

import db_funcs_for_site_parser as db
import excel_parser
import main


class Site_parser():

    def is_changed(self, new_file_link):
        name_of_course = self.get_name_of_course(new_file_link)
        current_file_link = db.get_current_link(name_of_course)
        if current_file_link != new_file_link:
            return True
        else:
            return False

    def is_file_exist(self, new_file_link):
        resp = requests.get(new_file_link)
        if resp.status_code == 200:
            return True
        else:
            return False

    def get_date_and_time_now(self):
        msc_timezone = pytz.timezone('Europe/Moscow')
        date_and_time_now = str(datetime.datetime.now(tz=msc_timezone))
        return date_and_time_now

    def create_new_excel_files(self, route, changed_files):
        for new_file_link in changed_files:
            if self.is_file_exist(new_file_link) == False:
                continue
            print('here new file link = ' + str(new_file_link))
            name_of_course = self.get_name_of_course(new_file_link)
            #if name_of_course == None:
            #    return None
            print('created new excel ' + str(name_of_course))
            self.create_table(route, name_of_course, new_file_link)

    def create_table(self, route, name_of_course, new_file_link):
        excel_file = open(f'time_tables/{route}/{name_of_course}.xlsx', 'wb')
        resp = requests.get(new_file_link)
        excel_file.write(resp.content)
        excel_file.close()

    def get_html_text(self):
        url = 'http://www.lesgaft.spb.ru/ru/schedule'
        resp = requests.get(url)
        return resp.text

    def get_soup_obj(self, html_text):
        soup_obj = BeautifulSoup(html_text, "lxml")
        return soup_obj


class Site_parser_undergraduate(Site_parser):

    def run_full_time_undergraduate_parser(self):
        files_from_site = self.get_all_files()
        self.create_new_excel_files('full_time_undergraduate', files_from_site)
        self.run_excel_parser()

    def get_all_files(self):
        file_links = []
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        lovs_links = self.get_lovs_links(soup_obj)
        zovs_links = self.get_zovs_links(soup_obj)
        file_links += lovs_links
        file_links += zovs_links
        return file_links


    def get_lovs_links(self, soup_obj):
        lovs_links = []
        element_1 = soup_obj.find_all('div', class_='views-row views-row-2 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_ = 'file')
        lovs_1_span = element_3[0]
        lovs_2_span = element_3[1]
        lovs_3_span = element_3[2]
        lovs_4_span = element_3[3]
        
        lovs_1_link = lovs_1_span.find_all('a', href=True)[0]['href']
        lovs_2_link = lovs_2_span.find_all('a', href=True)[0]['href']
        lovs_3_link = lovs_3_span.find_all('a', href=True)[0]['href']
        lovs_4_link = lovs_4_span.find_all('a', href=True)[0]['href']

        lovs_links.append(lovs_1_link)
        lovs_links.append(lovs_2_link)
        lovs_links.append(lovs_3_link)
        lovs_links.append(lovs_4_link)
        
        return lovs_links

    def get_zovs_links(self, soup_obj):
        zovs_links = []
        element_1 = soup_obj.find_all('div', class_='views-row views-row-3 views-row-odd')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_ = 'file')
        zovs_1_span = element_3[0]
        zovs_2_span = element_3[1]
        zovs_3_span = element_3[2]
        zovs_4_span = element_3[3]
        
        zovs_1_link = zovs_1_span.find_all('a', href=True)[0]['href']
        zovs_2_link = zovs_2_span.find_all('a', href=True)[0]['href']
        zovs_3_link = zovs_3_span.find_all('a', href=True)[0]['href']
        zovs_4_link = zovs_4_span.find_all('a', href=True)[0]['href']

        zovs_links.append(zovs_1_link)
        zovs_links.append(zovs_2_link)
        zovs_links.append(zovs_3_link)
        zovs_links.append(zovs_4_link)
        return zovs_links

    def get_name_of_course(self, file_link):
        course_names = ['1_lovs', '1_zovs', '2_lovs', '2_zovs',
                        '3_lovs', '3_zovs', '4_lovs', '4_zovs']
        for name in course_names:
            if name in file_link:
                return name

    def run_excel_parser(self):
        parser = excel_parser.Excel_parser()
        text = parser.run_parser('full_time_undergraduate')
        if text:
            main.send_custom_message_to_user(
                206171081, text)

class Site_parser_undergraduate_imst(Site_parser):

    def run_full_time_undergraduate_imst_parser(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        changed_files = self.find_changed_files(soup_obj)
        if len(changed_files) > 0:
            main.send_custom_message_to_user(
                206171081, f'Новые расписания: {changed_files}')

            self.create_new_excel_files(
                'full_time_undergraduate/imst', changed_files)
            self.run_excel_parser(changed_files)
        else:
            main.send_custom_message_to_user(
                206171081, 'Изменений расписаний в ИМИСТЕ не обнаружено')

    def find_changed_files(self, soup_obj):
        changed_files = []
        links_from_site = self.return_file_links_from_site_imst(soup_obj)

        for number in range(4):
            new_file_link = links_from_site[number]
            if self.is_changed(new_file_link):
                changed_files.append(new_file_link)
        return changed_files

    def return_file_links_from_site_imst(self, soup_obj):

        element = soup_obj.find_all(
            'div', class_=f'views-row views-row-10 views-row-even')
        element_2 = element[0].find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')
        imst_1 = element_2[0].find_all('a', href=True)[0]['href']
        imst_2 = element_2[0].find_all('a', href=True)[1]['href']
        imst_3 = element_2[0].find_all('a', href=True)[2]['href']
        imst_4 = element_2[0].find_all('a', href=True)[3]['href']

        return imst_1, imst_2, imst_3, imst_4

    def get_name_of_course(self, file_link):
        course_names = ['1_kurs_imst', '2_kurs_imst', '3_kurs_imst', '4_kurs_imst',
                        '1_kurs_imist', '2_kurs_imist', '3_kurs_imist', '4_kurs_imist']
        for name in course_names:
            if name in file_link:
                name_of_course = self.formate_name(name)
                return name_of_course

    def formate_name(self, name):
        if len(name) == 12:
            name = name.replace('imist', 'imst')
        first_part = name[:6]
        second_part = name[-4:]
        name_of_course = second_part + '_' + first_part
        return name_of_course

    def run_excel_parser(self, changed_files):
        for new_file_link in changed_files:
            name_of_course = self.get_name_of_course(new_file_link)
            parser = excel_parser.Excel_parser_undergraduate_imst()
            parser.parse_work_file_using_name(
                name_of_course, 'full_time_undergraduate/imst')


class Site_parser_magistracy_fk(Site_parser):

    def run_full_time_magistracy_fk(self):

        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files(
                'full_time_magistracy_fk', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_fk(self, number_of_course):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        element = soup_obj.find_all(
            'div', class_=f'views-row views-row-11 views-row-odd')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_='field-item even')
            try:
                new_file_link = element_2[1].find_all('a', href=True)[
                    0]['href']
            except IndexError:
                new_file_link = element_2[2].find_all('a', href=True)[
                    0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_='field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_fk(
                number)
            print(new_file_link)
            if self.is_changed(new_file_link):
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
            parser.parse_work_file_using_name(
                name_of_course, 'full_time_magistracy_fk')


class Site_parser_magistracy_afk(Site_parser):

    def run_full_time_magistracy_afk(self):

        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files(
                'full_time_magistracy_afk', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_afk(self, number_of_course):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        element = soup_obj.find_all(
            'div', class_=f'views-row views-row-12 views-row-even')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_='field-item even')
            new_file_link = element_2[1].find_all('a', href=True)[0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_='field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_afk(
                number)
            print(new_file_link)
            if self.is_changed(new_file_link):
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
            parser.parse_work_file_using_name(
                name_of_course, 'full_time_magistracy_afk')


class Site_parser_magistracy_imst(Site_parser):

    def run_full_time_magistracy_imst(self):
        changed_files = self.find_changed_files()
        if len(changed_files) > 0:
            self.create_new_excel_files(
                'full_time_magistracy_imst', changed_files)
            self.run_excel_parser(changed_files)

    def return_file_link_full_time_magistracy_imst(self, number_of_course):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        element = soup_obj.find_all(
            'div', class_=f'views-row views-row-13 views-row-odd')
        if number_of_course == 0:
            element_2 = element[0].find_all('div', class_='field-item even')
            new_file_link = element_2[1].find_all('a', href=True)[0]['href']
        elif number_of_course == 1:
            element_2 = element[0].find_all('div', class_='field-item odd')
            new_file_link = element_2[0].find_all('a', href=True)[0]['href']
        return new_file_link

    def find_changed_files(self):
        changed_files = []

        for number in range(2):
            new_file_link = self.return_file_link_full_time_magistracy_imst(
                number)
            print(new_file_link)
            if self.is_changed(new_file_link):
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
            parser.parse_work_file_using_name(
                name_of_course, 'full_time_magistracy_fk')


def run_undergraduate_parser():
    parser = Site_parser_undergraduate()
    parser.run_full_time_undergraduate_parser()


def run_undergraduate_parser_without_checking_changed_files():
    parser = Site_parser_undergraduate()
    parser.run_full_time_undergraduate_parser_without_checking_changed_files()


def run_undergraduate_imst_parser():
    parser = Site_parser_undergraduate_imst()
    parser.run_full_time_undergraduate_imst_parser()


def run_magistracy_fk_parser():
    parser = Site_parser_magistracy_fk()
    parser.run_full_time_magistracy_fk()


def run_magistracy_afk_parser():
    parser = Site_parser_magistracy_afk()
    parser.run_full_time_magistracy_afk()


def run_magistracy_imst_parser():
    parser = Site_parser_magistracy_imst()
    parser.run_full_time_magistracy_imst()


def run_all_parsers():
    parser_1 = Site_parser_undergraduate()
    parser_1.run_full_time_undergraduate_parser()
    parser_2 = Site_parser_undergraduate_imst()
    parser_2.run_full_time_undergraduate_imst_parser()
    parser_3 = Site_parser_magistracy_fk()
    parser_3.run_full_time_magistracy_fk()
    parser_4 = Site_parser_magistracy_afk()
    parser_4.run_full_time_magistracy_afk()
    parser_5 = Site_parser_magistracy_imst()
    parser_5.run_full_time_magistracy_imst()


def tested_run_all_parsers_with_all_new_links():
    db.drop_and_create_current_links_db()
    parser_1 = Site_parser_undergraduate()
    parser_1.run_full_time_undergraduate_parser()
    parser_2 = Site_parser_undergraduate_imst()
    parser_2.run_full_time_undergraduate_imst_parser()
    parser_3 = Site_parser_magistracy_fk()
    parser_3.run_full_time_magistracy_fk()
    parser_4 = Site_parser_magistracy_afk()
    parser_4.run_full_time_magistracy_afk()
    parser_5 = Site_parser_magistracy_imst()
    parser_5.run_full_time_magistracy_imst()


if __name__ == "__main__":
    run_undergraduate_parser()
