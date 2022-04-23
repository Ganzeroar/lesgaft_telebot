import os

import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'excel_validators'))

import requests
import datetime
import pytz
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
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_all_links(soup_obj)
        self.create_new_excel_files('full_time_undergraduate', files_from_site)
        text = self.run_excel_parser()
        return text

    def get_all_links(self, soup_obj):
        file_links = []

        lovs_links = self.get_lovs_links(soup_obj)
        zovs_links = self.get_zovs_links(soup_obj)
        file_links += lovs_links
        file_links += zovs_links
        return file_links

    def get_lovs_links(self, soup_obj):
        lovs_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-2 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
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
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-3 views-row-odd')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
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
        if bool(text):
            main.send_custom_message_to_user(
                206171081, text)
            return text


class Site_parser_undergraduate_imist(Site_parser):

    def run_full_time_undergraduate_imst_parser(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_imist_links(soup_obj)
        self.create_new_excel_files(
            'full_time_undergraduate_imist', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_imist_links(self, soup_obj):
        imist_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-5 views-row-odd')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        imist_1_span = element_3[0]
        imist_2_span = element_3[1]
        imist_3_span = element_3[2]
        imist_4_span = element_3[3]

        imist_1_link = imist_1_span.find_all('a', href=True)[0]['href']
        imist_2_link = imist_2_span.find_all('a', href=True)[0]['href']
        imist_3_link = imist_3_span.find_all('a', href=True)[0]['href']
        imist_4_link = imist_4_span.find_all('a', href=True)[0]['href']

        imist_links.append(imist_1_link)
        imist_links.append(imist_2_link)
        imist_links.append(imist_3_link)
        imist_links.append(imist_4_link)

        return imist_links

    def get_name_of_course(self, file_link):
        course_names = ['1_imist', '2_imist', '3_imist', '4_imist']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')


class Site_parser_undergraduate_afk(Site_parser):

    def run_full_time_undergraduate_imst_parser(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_afk_links(soup_obj)
        self.create_new_excel_files(
            'full_time_undergraduate_afk', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_afk_links(self, soup_obj):
        afk_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-4 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        afk_1_span = element_3[0]
        afk_2_span = element_3[1]
        afk_3_span = element_3[2]
        afk_4_span = element_3[3]

        afk_1_link = afk_1_span.find_all('a', href=True)[0]['href']
        afk_2_link = afk_2_span.find_all('a', href=True)[0]['href']
        afk_3_link = afk_3_span.find_all('a', href=True)[0]['href']
        afk_4_link = afk_4_span.find_all('a', href=True)[0]['href']

        afk_links.append(afk_1_link)
        afk_links.append(afk_2_link)
        afk_links.append(afk_3_link)
        afk_links.append(afk_4_link)

        return afk_links

    def get_name_of_course(self, file_link):
        course_names = ['1_afk', '2_afk', '3_afk', '4_afk']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')


class Site_parser_magistracy_fk(Site_parser):

    def run_full_time_magistracy_fk(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_magistracy_fk_links(soup_obj)
        self.create_new_excel_files(
            'full_time_magistracy_fk', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_magistracy_fk_links(self, soup_obj):
        mag_fk_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-6 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        mag_fk_1_span = element_3[1]
        mag_fk_2_span = element_3[3]

        mag_fk_1_link = mag_fk_1_span.find_all('a', href=True)[0]['href']
        mag_fk_2_link = mag_fk_2_span.find_all('a', href=True)[0]['href']

        mag_fk_links.append(mag_fk_1_link)
        mag_fk_links.append(mag_fk_2_link)

        return mag_fk_links

    def get_name_of_course(self, file_link):
        course_names = ['1_mag_fk', '2_mag_fk']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')


class Site_parser_magistracy_sport(Site_parser):

    def run_full_time_magistracy_sport(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_magistracy_sport_links(soup_obj)
        self.create_new_excel_files(
            'full_time_magistracy_sport', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_magistracy_sport_links(self, soup_obj):
        mag_sport_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-6 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        mag_sport_1_span = element_3[0]
        mag_sport_2_span = element_3[2]

        mag_sport_1_link = mag_sport_1_span.find_all('a', href=True)[0]['href']
        mag_sport_2_link = mag_sport_2_span.find_all('a', href=True)[0]['href']

        mag_sport_links.append(mag_sport_1_link)
        mag_sport_links.append(mag_sport_2_link)

        return mag_sport_links

    def get_name_of_course(self, file_link):
        course_names = ['1_mag_sport', '2_mag_sport']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')

class Site_parser_magistracy_afk(Site_parser):

    def run_full_time_magistracy_afk(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_magistracy_afk_links(soup_obj)
        self.create_new_excel_files(
            'full_time_magistracy_afk', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_magistracy_afk_links(self, soup_obj):
        mag_afk_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-7 views-row-odd')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        mag_afk_1_span = element_3[0]
        mag_afk_2_span = element_3[1]

        mag_afk_1_link = mag_afk_1_span.find_all('a', href=True)[0]['href']
        mag_afk_2_link = mag_afk_2_span.find_all('a', href=True)[0]['href']

        mag_afk_links.append(mag_afk_1_link)
        mag_afk_links.append(mag_afk_2_link)

        return mag_afk_links

    def get_name_of_course(self, file_link):
        course_names = ['1_mag_afk', '2_mag_afk']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')

class Site_parser_magistracy_imist(Site_parser):

    def run_full_time_magistracy_imist(self):
        html_text = self.get_html_text()
        soup_obj = self.get_soup_obj(html_text)

        files_from_site = self.get_magistracy_imist_links(soup_obj)
        self.create_new_excel_files(
            'full_time_magistracy_imist', files_from_site)
        self.run_excel_parser(files_from_site)

    def get_magistracy_imist_links(self, soup_obj):
        mag_imist_links = []
        element_1 = soup_obj.find_all(
            'div', class_='views-row views-row-8 views-row-even')[0]
        element_2 = element_1.find_all(
            'div', class_='field field-name-field-fl1 field-type-file field-label-hidden')[0]
        element_3 = element_2.find_all('span', class_='file')
        mag_imist_1_span = element_3[0]
        mag_imist_2_span = element_3[1]

        mag_imist_1_link = mag_imist_1_span.find_all('a', href=True)[0]['href']
        mag_imist_2_link = mag_imist_2_span.find_all('a', href=True)[0]['href']

        mag_imist_links.append(mag_imist_1_link)
        mag_imist_links.append(mag_imist_2_link)

        return mag_imist_links

    def get_name_of_course(self, file_link):
        course_names = ['1_mag_imist', '2_mag_imist']
        for name in course_names:
            if name in file_link:
                return name

    # TODO написать парсер, сейчас ссылается на что-то устаревшее
    # def run_excel_parser(self, changed_files):
    #    for new_file_link in changed_files:
    #        name_of_course = self.get_name_of_course(new_file_link)
    #        parser = excel_parser.Excel_parser_undergraduate_imst()
    #        parser.parse_work_file_using_name(
    #            name_of_course, 'full_time_undergraduate/imst')



def run_undergraduate_parser():
    parser = Site_parser_undergraduate()
    text = parser.run_full_time_undergraduate_parser()
    return text


def run_undergraduate_parser_without_checking_changed_files():
    parser = Site_parser_undergraduate()
    parser.run_full_time_undergraduate_parser_without_checking_changed_files()


def run_undergraduate_imist_parser():
    parser = Site_parser_undergraduate_imist()
    parser.run_full_time_undergraduate_imst_parser()


def run_magistracy_fk_parser():
    parser = Site_parser_magistracy_fk()
    parser.run_full_time_magistracy_fk()

def run_magistracy_sport_parser():
    parser = Site_parser_magistracy_sport()
    parser.run_full_time_magistracy_sport()

def run_magistracy_afk_parser():
    parser = Site_parser_magistracy_afk()
    parser.run_full_time_magistracy_afk()


def run_magistracy_imist_parser():
    parser = Site_parser_magistracy_imist()
    parser.run_full_time_magistracy_imist()


def run_all_parsers():
    parser_1 = Site_parser_undergraduate()
    parser_1.run_full_time_undergraduate_parser()
    parser_2 = Site_parser_undergraduate_imist()
    parser_2.run_full_time_undergraduate_imst_parser()
    parser_3 = Site_parser_magistracy_fk()
    parser_3.run_full_time_magistracy_fk()
    parser_4 = Site_parser_magistracy_afk()
    parser_4.run_full_time_magistracy_afk()
    parser_5 = Site_parser_magistracy_imist()
    parser_5.run_full_time_magistracy_imst()


def tested_run_all_parsers_with_all_new_links():
    db.drop_and_create_current_links_db()
    parser_1 = Site_parser_undergraduate()
    parser_1.run_full_time_undergraduate_parser()
    parser_2 = Site_parser_undergraduate_imist()
    parser_2.run_full_time_undergraduate_imst_parser()
    parser_3 = Site_parser_magistracy_fk()
    parser_3.run_full_time_magistracy_fk()
    parser_4 = Site_parser_magistracy_afk()
    parser_4.run_full_time_magistracy_afk()
    parser_5 = Site_parser_magistracy_imist()
    parser_5.run_full_time_magistracy_imst()


if __name__ == "__main__":
    run_magistracy_imist_parser()
