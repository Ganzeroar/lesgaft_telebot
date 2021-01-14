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
        except:
            pass
        db_funcs_for_students_db.create_db()
        db_funcs_for_students_db.starting_insert_data(111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(333333333, 'Ganzeroar3', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 417)
        db_funcs_for_students_db.update_group(333333333, 416)

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['группа_417'])
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')
        
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1 Зал№2')
    

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
    
    @freeze_time('2019-01-11 09:45:00')
    def test_today_subjects_equal_none_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 0, date)
        self.assertEqual(result, texts_for_lesgaft_bot.error)
    
    # По мск время +3, значит тут фактически 06:00:00    
    @freeze_time('2019-01-09 06:00:00')
    @patch('find_class_location.find_class_location', return_value = 'путь')
    def test_when_before_lessons_return_correct_data(self, find_class_location):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся\nпредмет1\n\nпуть')
    
    @freeze_time('2019-01-09 06:00:00')
    @patch('find_class_location.find_class_location', return_value = 'путь')
    def test_when_before_lessons_return_correct_data_new_db_column_names(self, find_class_location):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(333333333, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся\nпредмет1\n\nпуть')
    
    @freeze_time('2019-01-10 06:00:00')
    def test_real_when_before_lessons_return_correct_data(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')

#@unittest.skip("passed")
class Test_find_lessons_at_date_return_lessons_at_date(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db()
            db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
        except:
            pass
        db_funcs_for_students_db.create_db()
        db_funcs_for_students_db.starting_insert_data(111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(333333333, 'Ganzeroar3', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 417)
        db_funcs_for_students_db.update_group(333333333, 416)


        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['группа_417'])
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')
        
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1 Зал№2')
        

        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '18:40')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.12.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.12.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '11.12.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '12.12.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '13.12.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.12.', '18:40')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '18:40', 'группа_417', 'предмет6')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.12.', '9:45', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.12.', '11:30', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '11.12.', '13:30', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '12.12.', '15:15', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '13.12.', '17:00', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.12.', '18:40', 'группа_417', 'нет предмета')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
    
    @freeze_time('2019-12-22 03:00:00')
    def test_get_sunday_return_sunday_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, date)
        self.assertEqual(result, 'Воскресенье, не учимся!')

    @freeze_time('2019-12-20 03:00:00')
    def test_user_not_in_bd_return_error_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, date)
        self.assertEqual(result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')
    
    @freeze_time('2019-12-20 03:00:00')
    def test_group_not_exist_return_error_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(222222222, date)
        self.assertEqual(result, 'Твоей группы не существует. Измени номер группы.')
    
    @freeze_time('2019-01-09 03:00:00')
    def test_5_subject_all_correct_return_correct_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result, expected_string)
    
    @freeze_time('2019-01-09 03:00:00')
    def test_new_db_column_names_return_correct_message(self):
        #тест для проверки новых имён столбиков в базе
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(333333333, date)
        expected_string = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result, expected_string)
    

    @freeze_time('2019-01-14 03:00:00')
    def test_6_subject_all_correct_return_correct_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'Расписание на понедельник (14.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n18:40-20:10\nпредмет6\n\n'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-09 03:00:00')
    def test_today_not_subjects_return_correct_message_in_monday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'В понедельник (09.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-10 03:00:00')
    def test_today_not_subjects_return_correct_message_in_tuesday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'Во вторник (10.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-11 03:00:00')
    def test_today_not_subjects_return_correct_message_in_wednesday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'В среду (11.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-12 03:00:00')
    def test_today_not_subjects_return_correct_message_in_thursday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'В четверг (12.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-13 03:00:00')
    def test_today_not_subjects_return_correct_message_in_friday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'В пятницу (13.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-12-14 03:00:00')
    def test_today_not_subjects_return_correct_message_in_saturday(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'В субботу (14.12.2019.) у тебя нет пар'
        self.assertEqual(result, expected_string)


class Test_find_class_location_find_class_location(unittest.TestCase):

    def test_take_correct_data_return_correct_data(self):
        result = find_class_location.find_class_location('ауд.426 Лекция Дисциплина по выбору')
        self.assertEqual(result, 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону')

    def test_take_real_correct_data_return_correct_data(self):
        real_data = '''ауд.421\nЛекция\nДисциплина по выбору'''
        result = find_class_location.find_class_location(real_data)
        self.assertEqual(result, 'Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону')

#@unittest.skip("not_need")
class Test_main(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db()
        except:
            pass
        db_funcs_for_students_db.create_db()
        db_funcs_for_students_db.starting_insert_data(111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 417)
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(111111111, True)
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(222222222, True)


    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()

    def test_return_subscribed_to_news_users_return_2(self):
        result = main.return_subscribed_to_news_users()
        self.assertEqual(len(result), 2)
        self.assertEqual(result, [(111111111,), (222222222,)])


    #@freeze_time('2019-01-10 03:00:00')
    #def test_return_where_is_the_lesson_take_correct_data_return_correct(self):
    #    result = main.return_where_is_the_lesson(111111111)
    #    date = datetime.datetime.now()
    #    self.assertEqual(result, ('Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж', 'main_keyboard'))
#
    #@freeze_time('2019-01-09 03:00:00')
    #def test_return_today_lessons_take_correct_data_return_correct(self):
    #    result = main.return_today_lessons(111111111)
    #    expected = ('Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n', 'main_keyboard')
    #    self.assertEqual(result, expected)
#
    #@freeze_time('2019-01-10 03:00:00')
    #def test_return_tomorrow_lessons_take_correct_data_return_correct(self):
    #    result = main.return_today_lessons(111111111)
    #    expected = ('Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n', 'main_keyboard')
    #    self.assertEqual(result, expected)
    #
    #def test_return_where_is_the_classroom_take_correct_data_return_correct(self):
    #    result = main.return_where_is_the_classroom(111111111, 'где 10')
    #    self.assertEqual(result, ('ИЭиСТ, первый этаж', 'main_keyboard'))
#
    #def test_change_group_step_1_take_correct_data_return_correct(self):
    #    first_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    #    full_time = telebot.types.KeyboardButton('Очное обучение321')
    #    part_time = telebot.types.KeyboardButton('Заочное обучение321')
    #    first_step_keyboard.add(full_time, part_time)
#
    #    result1 = main.change_group_step_1(111111111)[0]
    #    result2 = main.change_group_step_1(111111111)[1]
#
    #    registration_process = db_funcs_for_students_db.get_state_of_registration_process(111111111)
    #    
    #    self.assertEqual(result1, 'Какая у тебя форма обучения?')
    #    self.assertEqual(type(result2), type(first_step_keyboard))
    #    self.assertEqual(registration_process, True)
#
    #def test_change_group_step_2_not_in_registration_process_return_error_message(self):
    #    result = main.change_group_step_2(222222222, 'Очное обучение')
    #    self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))
#
    #def test_change_group_step_2_take_correct_data_return_correct(self):
    #    second_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    #    undergraduate = telebot.types.KeyboardButton('Бакалавриат')
    #    magistracy = telebot.types.KeyboardButton('Магистратура')
    #    second_step_keyboard.add(undergraduate, magistracy)
#
    #    main.change_group_step_1(111111111)
    #    registration_process = db_funcs_for_students_db.get_state_of_registration_process(111111111)
    #    result1 = main.change_group_step_2(111111111, 'Очное обучение')[0]
    #    result2 = main.change_group_step_2(111111111, 'Очное обучение')[1]
    #    
    #    education_form = db_funcs_for_students_db.get_education_form(111111111)
#
    #    self.assertEqual(result1, 'На каком направлении ты учишься?')
    #    self.assertEqual(type(result2), type(second_step_keyboard))
    #    self.assertEqual(education_form, 'Очное обучение')
    #    
    #def test_change_group_step_3_not_in_registration_process_return_error_message(self):
    #    result = main.change_group_step_3(222222222, 'Очное обучение')
    #    self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))
#
    #def test_change_group_step_3_take_undergraduate_return_correct(self):
    #    main.change_group_step_1(111111111)
    #    
    #    third_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    #    course_1 = telebot.types.KeyboardButton('1 курс')
    #    course_2 = telebot.types.KeyboardButton('2 курс')
    #    course_3 = telebot.types.KeyboardButton('3 курс')
    #    course_4 = telebot.types.KeyboardButton('4 курс')
    #    third_step_keyboard.add(course_1, course_2, course_3, course_4)
#
    #    result1 = main.change_group_step_3(111111111, 'бакалавриат')[0]
    #    result2 = main.change_group_step_3(111111111, 'бакалавриат')[1]
#
    #    academic_degree = db_funcs_for_students_db.get_academic_degree(111111111)
#
    #    self.assertEqual(result1, 'На каком курсе ты учишься?')
    #    self.assertEqual(type(result2), type(third_step_keyboard))
    #    self.assertEqual(academic_degree, 'бакалавриат')
    #    
    #def test_change_group_step_3_take_magistracy_return_correct(self):
    #    main.change_group_step_1(111111111)
#
    #    third_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    #    course_1 = telebot.types.KeyboardButton('1 курс')
    #    course_2 = telebot.types.KeyboardButton('2 курс')
    #    third_step_keyboard.add(course_1, course_2)
#
    #    result1 = main.change_group_step_3(111111111, 'магистратура')[0]
    #    result2 = main.change_group_step_3(111111111, 'магистратура')[1]
#
    #    academic_degree = db_funcs_for_students_db.get_academic_degree(111111111)
#
    #    self.assertEqual(result1, 'На каком курсе ты учишься?')
    #    self.assertEqual(type(result2), type(third_step_keyboard))
    #    self.assertEqual(academic_degree, 'магистратура')
    #    
    #def test_change_group_step_4_not_in_registration_process_return_error_message(self):
    #    result = main.change_group_step_3(222222222, '1 курс')
    #    self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))
#
    #def test_change_group_step_4_take_undergraduate_return_correct(self):
    #    main.change_group_step_1(111111111)
#
    #    fourth_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    #    first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag)
    #    second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_afk)
    #    third_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_tour)
#
    #    result1 = main.change_group_step_4(111111111, '1 курс')[0]
    #    result2 = main.change_group_step_4(111111111, '1 курс')[1]
#
    #    number_of_course = db_funcs_for_students_db.get_number_of_course(111111111)
#
    #    self.assertEqual(result1, 'Как называется твоё расписание на сайте?')
    #    self.assertEqual(type(result2), type(fourth_step_keyboard))
    #    self.assertEqual(number_of_course, 1)

        
#@unittest.skip("passed")
class Test_site_parser_undergraduate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_site_parser.drop_db()
        except:
            pass
        
        db_funcs_for_site_parser.create_db()
        db_funcs_for_site_parser.insert_link_to_current_links()
        db_funcs_for_site_parser.change_link_in_current_links('lovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._20.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('zovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_zovs_-_2_sem._17.02.xlsx')

        db_funcs_for_site_parser.change_link_in_current_links('zovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_zovs.xls')
        db_funcs_for_site_parser.change_link_in_current_links('lovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_lovs.xlsx')
        
        db_funcs_for_site_parser.change_link_in_current_links('zovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._20.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('lovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_lovs_-_2_sem._19.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('zovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_zovs_19.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('lovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.03.xlsx')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_site_parser.drop_db()

    def test_is_changed_return_true(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.is_changed('http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._25.02.xlsx')
        self.assertEqual(result, True)

    def test_is_changed_return_false(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.is_changed('http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._20.02.xlsx')
        self.assertEqual(result, False)

    @patch.object(site_parser.Site_parser, 'is_file_exist')
    def test_find_changed_files_return_4_changed_file_link(self, is_file_exist_mock):
        is_file_exist_mock.return_value = 200 
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.find_changed_files(soup_obj)
        self.assertEqual(len(result), 4)
        self.assertEqual(result, ['http://www.lesgaft.spb.ru/sites/default/files//shedul//2_kurs_lovs_19.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_kurs_zovs_19.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._17.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx'])

    def test_get_file_link_from_site_full_time_undergraduate_return_filelink(self):
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.get_file_link_from_site_full_time_undergraduate(7, soup_obj)
        self.assertEqual(result, 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._17.02.xlsx')

    def test_find_file_link_return_correct_link(self):
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.find_file_link(8, soup_obj)
        self.assertEqual(result, 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx')

    def test_create_html_string_return_correct_string_odd(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.create_html_string(5)
        self.assertEqual(result, 'views-row views-row-5 views-row-odd')

    def test_create_html_string_return_correct_string_even(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.create_html_string(2)
        self.assertEqual(result, 'views-row views-row-2 views-row-even')

    def test_get_name_of_course_return_correct(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.get_name_of_course('http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx')
        self.assertEqual(result, 'lovs_4_kurs')

    #Тест на обход бага, когда учебный отдел приделывает 'int' к расписанию
    def test_get_name_of_course_int_bag_return_correct(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.get_name_of_course('http://lesgaft.spb.ru/sites/default/files//shedul//3_kurs_int_07.10.xlsx')
        self.assertEqual(result, 'zovs_3_kurs')
        
    def test_formate_name_return_correct(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.formate_name('3_kurs_zovs')
        self.assertEqual(result, 'zovs_3_kurs')

#@unittest.skip("passed")
class Test_site_parser_undergraduate_imist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_site_parser.drop_db()
        except:
            pass
        
        db_funcs_for_site_parser.create_db()
        db_funcs_for_site_parser.insert_link_to_current_links()
        db_funcs_for_site_parser.change_link_in_current_links('imst_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_1_kurs_imst_17.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('imst_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_2_kurs_imst_05.12.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('imst_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_3_kurs_imst_13.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links('imst_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_4_kurs_imst_05.12.xlsx')
        #http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_3_kurs_imst_13.02.xlsx
        #db_funcs_for_site_parser.change_link_in_current_links('zovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_zovs.xls')
        #db_funcs_for_site_parser.change_link_in_current_links('lovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_lovs.xlsx')
        #
        #db_funcs_for_site_parser.change_link_in_current_links('zovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._20.02.xlsx')
        #db_funcs_for_site_parser.change_link_in_current_links('lovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_lovs_-_2_sem._19.02.xlsx')
        #db_funcs_for_site_parser.change_link_in_current_links('zovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_zovs_19.02.xlsx')
        #db_funcs_for_site_parser.change_link_in_current_links('lovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.03.xlsx')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_site_parser.drop_db()

    def test_is_changed_return_true(self):
        obj = site_parser.Site_parser_undergraduate_imst()
        result = obj.is_changed('http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_2_kurs_imst_13.02.xlsx')
        self.assertEqual(result, True)

    def test_find_changed_files_return_2_changed_file_link(self):
        obj = site_parser.Site_parser_undergraduate_imst()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.find_changed_files(soup_obj)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ['http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_2_kurs_imst_13.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_4_kurs_imst_14.02.xlsx'])

    def test_return_file_link_from_site_imst_return_filelink(self):
        obj = site_parser.Site_parser_undergraduate_imst()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.return_file_links_from_site_imst(soup_obj)
        self.assertEqual(result, ('http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_1_kurs_imst_17.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_2_kurs_imst_13.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_3_kurs_imst_13.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//raspisanie_4_kurs_imst_14.02.xlsx'))
#
    #def test_find_file_link_return_correct_link(self):
    #    obj = site_parser.Site_parser_undergraduate()
    #    soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
    #    result = obj.find_file_link(8, soup_obj)
    #    self.assertEqual(result, 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx')
#
    #def test_create_html_string_return_correct_string_odd(self):
    #    obj = site_parser.Site_parser_undergraduate()
    #    result = obj.create_html_string(5)
    #    self.assertEqual(result, 'views-row views-row-5 views-row-odd')
#
    #def test_create_html_string_return_correct_string_even(self):
    #    obj = site_parser.Site_parser_undergraduate()
    #    result = obj.create_html_string(2)
    #    self.assertEqual(result, 'views-row views-row-2 views-row-even')
#
    #def test_get_name_of_course_return_correct(self):
    #    obj = site_parser.Site_parser_undergraduate()
    #    result = obj.get_name_of_course('http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx')
    #    self.assertEqual(result, 'lovs_4_kurs')
#
    #def test_formate_name_return_correct(self):
    #    obj = site_parser.Site_parser_undergraduate()
    #    result = obj.formate_name('3_kurs_zovs')
    #    self.assertEqual(result, 'zovs_3_kurs')


#@unittest.skip("broken")
class Test_excel_parser_undergraduate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configurations.month_to_skip = ['01', '02', '03']
#
    #@classmethod
    #def tearDownClass(cls):
    #    configurations.month_to_skip = ['09', '10', '11', '12', '01', '02']
#
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    def test_format_date_return_correct(self):
        parser = excel_parser.Excel_parser()
        date = """05.09.
                12.09.
                19.09."""
        result = parser.format_dates(date)
        self.assertEqual(result, ['05.09.', '12.09.', '19.09.'])
        
        date_incorrect = "10.10 17.10 24.10"
        result_2 = parser.format_dates(date_incorrect)
        self.assertEqual(result_2, ['10.10.', '17.10.', '24.10.'])

    def test_is_in_month_to_skip(self):
        work_sheet_names = ['<Worksheet "с 05.01>"', '<Worksheet "с ауд. 28.09-03.02>"', '<Worksheet "с  07.09. - 26.03.>"', '<Worksheet "с ауд. 30.11.-05.01.>"', '<Worksheet "ПОКА БЕЗ АУД. с 21.12.-26.02>"']
        obj = excel_parser.Excel_parser()
        for name in work_sheet_names:
            result = obj.is_reason_to_skip(name)
            self.assertTrue(result)

    def test_format_group_name(self):
        names_from_excel = texts_for_tests.group_names_from_excel
        normal_group_names = texts_for_tests.normal_group_names
        obj = excel_parser.Excel_parser()
        for x in range(len(normal_group_names)):
            normal_name = normal_group_names[x]
            excel_name = names_from_excel[x]
            formatted_name = obj.format_group_name(excel_name)
            self.assertEqual(normal_name, formatted_name)

    #@unittest.skip("passed")
    def test_undergraduate_parser(self):
        parser = excel_parser.Excel_parser()
        groups_and_expected_number_of_records = {
            'zovs_1_kurs' : 31,
            'zovs_2_kurs' : 35,
            'zovs_3_kurs' : 35,
            'zovs_4_kurs' : 34,
            'lovs_1_kurs' : 35,
            'lovs_2_kurs' : 32,
            'lovs_3_kurs' : 32,
            'lovs_4_kurs' : 32,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_undergraduate')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            print(couple)
            self.assertEqual(expected_number_of_record, actual_number_of_record)

    #@unittest.skip("passed")
    def test_imst_parser(self):
        parser = excel_parser.Excel_parser_undergraduate_imst()
        groups_and_expected_number_of_records = {
            'imst_1_kurs' : 36,
            'imst_2_kurs' : 36,
            'imst_3_kurs' : 36,
            'imst_4_kurs' : 36,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_undergraduate/imst')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            print(couple)
            self.assertEqual(expected_number_of_record, actual_number_of_record)

    #@unittest.skip("passed")
    def test_mag_fk(self):
        parser = excel_parser.Excel_parser()
        groups_and_expected_number_of_records = {
            'magistracy_fk_full_time_1_kurs' : 36,
            'magistracy_fk_full_time_2_kurs' : 36,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_magistracy_fk')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            print(couple)
            self.assertEqual(expected_number_of_record, actual_number_of_record)

    #@unittest.skip("passed")
    def test_mag_afk(self):
        parser = excel_parser.Excel_parser()
        groups_and_expected_number_of_records = {
            'magistracy_afk_full_time_1_kurs' : 36,
            'magistracy_afk_full_time_2_kurs' : 36,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_magistracy_afk')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            print(couple)
            self.assertEqual(expected_number_of_record, actual_number_of_record)

    #@unittest.skip("passed")
    def test_mag_imst(self):
        parser = excel_parser.Excel_parser()
        groups_and_expected_number_of_records = {
            'magistracy_imst_full_time_1_kurs' : 36,
            'magistracy_imst_full_time_2_kurs' : 36,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_magistracy_imst')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            print(couple)
            self.assertEqual(expected_number_of_record, actual_number_of_record)

class Test_db_funcs_for_subjects_db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db()
            db_funcs_for_subjects_db.drop_db('zovs_4_kurs')

            os.remove('wrong_timetables_reports.log')
        except:
            pass

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['группа_417'])
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1 Зал№2')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
    
    @freeze_time('2019-01-10 03:00:00')
    def test_get_db_name_take_correct_return_correct(self):
        result = db_funcs_for_subjects_db.get_db_name('группа_417')
        self.assertEqual(result, 'zovs_4_kurs')
        
        result = db_funcs_for_subjects_db.get_db_name('конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416')
        self.assertEqual(result, 'zovs_4_kurs')
        
    def test_isgroup_exist(self):
        result = db_funcs_for_subjects_db.is_group_exist('группа_417', 'zovs_4_kurs')
        self.assertTrue(result)
        
        result = db_funcs_for_subjects_db.is_group_exist('группа_416', 'zovs_4_kurs')
        self.assertTrue(result)

    def test_return_new_group_name(self):
        result = db_funcs_for_subjects_db.return_new_group_name('группа_416', 'zovs_4_kurs')
        self.assertEqual(result, 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416')
        

#@unittest.skip("passed")
class Test_request_handler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db()
            db_funcs_for_subjects_db.drop_db('zovs_4_kurs')

            os.remove('wrong_timetables_reports.log')
        except:
            pass
        db_funcs_for_students_db.create_db()
        db_funcs_for_students_db.starting_insert_data(111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 417)
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(222222222, True)

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['группа_417'])
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')
        
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '18:40')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '18:40', 'группа_417', 'предмет6')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4_kurs')
    
    @freeze_time('2019-01-10 03:00:00')
    def test_return_where_is_the_lesson_take_correct_data_return_correct(self):
        result = request_handler.return_where_is_the_lesson(111111111)
        self.assertEqual(result[0], 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-10 03:00:00')
    def test_main_request_handler_take_where_is_the_lesson_request_return_correct(self):
        result = request_handler.main_request_handler('Где пара?', 111111111)
        self.assertEqual(result[0], 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-09 03:00:00')
    def test_return_today_lessons_take_correct_data_return_correct(self):
        result = request_handler.return_today_lessons(111111111)
        expected_text = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-09 03:00:00')
    def test_main_request_handler_take_today_lessons_request_return_correct(self):
        result = request_handler.main_request_handler('Какие сегодня пары?', 111111111)
        expected_text = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-10 03:00:00')
    def test_return_tomorrow_lessons_take_correct_data_return_correct(self):
        result = request_handler.return_today_lessons(111111111)
        expected_text = 'Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])
    
    @freeze_time('2019-01-09 03:00:00')
    def test_main_request_handler_take_tomorrow_lessons_request_return_correct(self):
        result = request_handler.main_request_handler('Какие завтра пары?', 111111111)
        expected_text = 'Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    def test_return_where_is_the_classroom_take_correct_data_return_correct(self):
        result = request_handler.return_where_is_the_classroom(111111111, 'где 10')
        self.assertEqual(result[0], 'ИЭиСТ, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_where_is_the_classroom_request_return_correct(self):
        result = request_handler.main_request_handler('где 10', 111111111)
        self.assertEqual(result[0], 'ИЭиСТ, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_return_to_menu_return_menu(self):
        result = request_handler.main_request_handler('Вернуться в меню', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_menu_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Расписание'}], [{'text': 'Настройки'}], [{'text': 'Что умеет ЛесгафтБот'}]])

    def test_main_request_handler_take_what_lesgaftbot_can_do_return_text(self):
        result = request_handler.main_request_handler('Что умеет ЛесгафтБот', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.what_lesgaftbot_can_do_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Расписание'}], [{'text': 'Настройки'}], [{'text': 'Что умеет ЛесгафтБот'}]])

    def test_main_request_handler_take_settings_and_user_not_in_news_subscribers_return_settins(self):
        result = request_handler.main_request_handler('Настройки', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписки и рассылки'}], [{'text': 'Связь с разработчиком'}],[{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_subscriptions_and_newsletter_return_text(self):
        result = request_handler.main_request_handler('Подписки и рассылки', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_subscriptions_and_newsletters_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписаться на рассылку новостей'}], [{'text': 'Информация о подписках'}], [{'text': 'Вернуться в настройки'}]])

    def test_main_request_handler_take_info_about_subscriptions_user_not_subscribe_return_correct_text(self):
        result = request_handler.main_request_handler('Информация о подписках', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.info_about_subscriptions_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписаться на рассылку новостей'}], [{'text': 'Информация о подписках'}], [{'text': 'Вернуться в настройки'}]])

    def test_main_request_handler_take_subsctibe_to_newsletter_then_in_bd_user_subscription_is_true(self):
        result = request_handler.main_request_handler('Подписаться на рассылку новостей', 111111111)
        status = db_funcs_for_students_db.get_subscribe_in_newsletter_status(111111111)
        self.assertEqual(result[0], 'Подписка активирована')
        self.assertEqual(result[1].keyboard, [[{'text': 'Отписаться от рассылки новостей'}], [{'text': 'Информация о подписках'}], [{'text': 'Вернуться в настройки'}]])
        self.assertEqual(status, True)
    
    def test_main_request_handler_take_settings_and_user_already_in_news_subscribers_return_correct_settins(self):
        result = request_handler.main_request_handler('Настройки', 222222222)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписки и рассылки'}], [{'text': 'Связь с разработчиком'}],[{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_info_about_subscriptions_user_subscribe_return_correct_text(self):
        result = request_handler.main_request_handler('Информация о подписках', 222222222)
        self.assertEqual(result[0], texts_for_lesgaft_bot.info_about_subscriptions_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Отписаться от рассылки новостей'}], [{'text': 'Информация о подписках'}], [{'text': 'Вернуться в настройки'}]])

    def test_main_request_handler_take_unsubsctibe_to_newsletter_then_in_bd_user_subscription_is_false(self):
        result = request_handler.main_request_handler('Отписаться от рассылки новостей', 222222222)
        db_funcs_for_students_db.set_is_subscribe_to_newsletter(222222222, False)
        status = db_funcs_for_students_db.get_subscribe_in_newsletter_status(222222222)
        self.assertEqual(result[0], 'Подписка отключена')
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписаться на рассылку новостей'}], [{'text': 'Информация о подписках'}], [{'text': 'Вернуться в настройки'}]])
        self.assertEqual(status, False)

    def test_main_request_handler_take_go_to_timetables_return_timetables_menu(self):
        result = request_handler.main_request_handler('Расписание', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_timetables_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-10 03:00:00')
    def test_main_request_handler_take_wrong_timetables_return_correct_text_and_save_in_logfile(self):
        result = request_handler.main_request_handler('Расписание неправильное', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.wrong_timetables)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [{'text': 'Какие завтра пары?'}],[{'text': 'Расписание неправильное'}] ,[{'text': 'Вернуться в меню'}]])
        with open('wrong_timetables_reports.log') as f:
            f = f.readlines()
        file_text = f
        
        assert_file_text = ['INFO:root:группа_417 10.01.2019.\n', "[('предмет1 Зал№2',)]\n", 'Юзер: 111111111\n']
        self.assertEqual(file_text, assert_file_text)

    def test_main_request_handler_take_communication_with_developer_return_text(self):
        result = request_handler.main_request_handler('Связь с разработчиком', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.communication_with_developer_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписки и рассылки'}], [{'text': 'Связь с разработчиком'}],[{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_return_to_settings_return_text(self):
        result = request_handler.main_request_handler('Вернуться в настройки', 111111111)
        self.assertEqual(result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Подписки и рассылки'}], [{'text': 'Связь с разработчиком'}],[{'text': 'Вернуться в меню'}]])



if __name__ == '__main__':
    unittest.main()