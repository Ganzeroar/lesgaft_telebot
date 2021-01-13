import unittest
import telebot
from unittest.mock import patch
from freezegun import freeze_time
import datetime
import glob
import pytz
import sqlite3
import os

import find_time_and_location
import find_lessons_at_date
import find_class_location
import main
import excel_parser
import request_handler
import site_parser
import configurations

import texts_for_tests
import texts_for_lesgaft_bot
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import db_funcs_for_site_parser

#class Test_excel_parser_and_request_handler

#@unittest.skip("passed")
class Test_find_time_and_location_return_location_of_class(unittest.TestCase):

    def test_take_long_str_return_error_text(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где string')
        self.assertEqual(result, 'Такой аудитории я не знаю')

    def test_take_str_return_error_text(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где str')
        self.assertEqual(result, texts_for_lesgaft_bot.invalid_text)

    @patch('find_class_location.find_class_location_used_number', return_value = 'путь')
    def test_take_correct_text_return_correct_way(self, find_class_location_used_number):
        result = find_time_and_location.return_location_of_class(123456789, 'где 222')
        self.assertEqual(result, 'путь')

    def test_take_correct_text_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где 10')
        self.assertEqual(result, 'ИЭиСТ, первый этаж')

    def test_take_correct_faculty_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где факультет зимних олимпийских видов спорта')
        self.assertEqual(result, 'Мойка, вход со стороны стадиона, третий этаж')

    def test_take_correct_department_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где кафедра теории и методики неолимпийских видов спорта')
        self.assertEqual(result, 'Мойка, третий этаж, после лестницы направо, по левую сторону')

#@unittest.skip("passed")
class Test_find_time_and_location_return_text_about_time_before_lesson_with_location(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db()
            db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
            db_funcs_for_subjects_db.drop_db('imst_4_kurs')
        except:
            pass
        db_funcs_for_students_db.create_db()
        db_funcs_for_students_db.starting_insert_data(111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(333333333, 'Ganzeroar3', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 'лыжный_спорт_биатлон_группа_417')
        db_funcs_for_students_db.update_group(333333333, 'реклама_и_связи_с_общественностью')

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['лыжный_спорт_биатлон_группа_417'])
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'лыжный_спорт_биатлон_группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'лыжный_спорт_биатлон_группа_417', 'предмет1 Зал№2')
        db_funcs_for_subjects_db.create_db('imst_4_kurs')
        db_funcs_for_subjects_db.save_groups('imst_4_kurs', ['реклама_и_связи_с_общественностью'])
        db_funcs_for_subjects_db.save_dates_and_times('imst_4_kurs', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('imst_4_kurs', '09.01.', '9:45', 'реклама_и_связи_с_общественностью', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times('imst_4_kurs', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('imst_4_kurs', '10.01.', '9:45', 'реклама_и_связи_с_общественностью', 'предмет1 Зал№2')

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
    
    def test_user_id_not_in_db_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 1, date)
        self.assertEqual(result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')
    
    def test_group_isnt_exist_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(222222222, 1, date)
        self.assertEqual(result, 'Такой группы не существует. Измени номер группы.')
    
    def test_num_of_lessons_bigger_then_6_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 6, date)
        self.assertEqual(result, 'Сегодня у тебя больше нет пар.')
    
    @freeze_time('2019-01-11 09:45:00')
    def test_today_subjects_equal_false_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 0, date)
        self.assertEqual(result, texts_for_lesgaft_bot.error)
