import unittest
import telebot
from unittest.mock import patch
from freezegun import freeze_time
import datetime
import glob
import pytz
import sqlite3

import find_time_and_location
import find_lessons_at_date
import find_class_location
import main
import site_parser_class
import excel_parser

import texts_for_tests
import texts_for_lesgaft_bot
import db_funcs_for_students_db
import db_funcs_for_subjects_db
import db_funcs_for_site_parser
@unittest.skip("passed")    
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
@unittest.skip("passed")    
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
        db_funcs_for_students_db.update_group(111111111, 417)

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['Группа_417'])
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'Группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times('zovs_4_kurs', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'Группа_417', 'предмет1 Зал№2')

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
        self.assertEqual(result, 'Через 3:45 начнётся предмет1\n\nпуть')
    
    @freeze_time('2019-01-10 06:00:00')
    def test_real_when_before_lessons_return_correct_data(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(111111111, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся предмет1 Зал№2\n\nМанеж, первый этаж')
@unittest.skip("passed")    
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
        db_funcs_for_students_db.update_group(111111111, 417)

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['Группа_417'])
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'Группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'Группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'Группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'Группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'Группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'Группа_417', 'предмет1 Зал№2')
        
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '18:40')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '9:45', 'Группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '11:30', 'Группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '13:30', 'Группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '15:15', 'Группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '17:00', 'Группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '18:40', 'Группа_417', 'предмет6')
        
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
    
    @freeze_time('2019-01-14 03:00:00')
    def test_6_subject_all_correct_return_correct_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'Расписание на понедельник (14.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n18:40-20:10\nпредмет6\n\n'
        self.assertEqual(result, expected_string)
class Test_find_class_location_find_class_location(unittest.TestCase):

    def test_take_correct_data_return_correct_data(self):
        result = find_class_location.find_class_location('ауд.426 Лекция Дисциплина по выбору')
        self.assertEqual(result, 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону')
@unittest.skip("passed")    
class Test_main(unittest.TestCase):
    
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
        db_funcs_for_students_db.update_group(111111111, 417)

        db_funcs_for_subjects_db.create_db('zovs_4_kurs')
        db_funcs_for_subjects_db.save_groups('zovs_4_kurs', ['Группа_417'])
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '9:45', 'Группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '11:30', 'Группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '13:30', 'Группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '15:15', 'Группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '09.01.', '17:00', 'Группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '10.01.', '9:45', 'Группа_417', 'предмет1 Зал№2')
        
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time('zovs_4_kurs', '14.01.', '18:40')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '9:45', 'Группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '11:30', 'Группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '13:30', 'Группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '15:15', 'Группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '17:00', 'Группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_subj('zovs_4_kurs', '14.01.', '18:40', 'Группа_417', 'предмет6')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4_kurs')

    @freeze_time('2019-01-10 03:00:00')
    def test_return_where_is_the_lesson_take_correct_data_return_correct(self):
        result = main.return_where_is_the_lesson(111111111)
        date = datetime.datetime.now()
        self.assertEqual(result, ('Через 3:45 начнётся предмет1 Зал№2\n\nМанеж, первый этаж', 'main_keyboard'))

    @freeze_time('2019-01-09 03:00:00')
    def test_return_today_lessons_take_correct_data_return_correct(self):
        result = main.return_today_lessons(111111111)
        expected = ('Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n', 'main_keyboard')
        self.assertEqual(result, expected)

    @freeze_time('2019-01-10 03:00:00')
    def test_return_tomorrow_lessons_take_correct_data_return_correct(self):
        result = main.return_today_lessons(111111111)
        expected = ('Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n', 'main_keyboard')
        self.assertEqual(result, expected)
    
    def test_return_where_is_the_classroom_take_correct_data_return_correct(self):
        result = main.return_where_is_the_classroom(111111111, 'где 10')
        self.assertEqual(result, ('ИЭиСТ, первый этаж', 'main_keyboard'))

    def test_change_group_step_1_take_correct_data_return_correct(self):
        first_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
        full_time = telebot.types.KeyboardButton('Очное обучение321')
        part_time = telebot.types.KeyboardButton('Заочное обучение321')
        first_step_keyboard.add(full_time, part_time)

        result1 = main.change_group_step_1(111111111)[0]
        result2 = main.change_group_step_1(111111111)[1]

        registragion_process = db_funcs_for_students_db.get_state_of_registragion_process(111111111)
        
        self.assertEqual(result1, 'Какая у тебя форма обучения?')
        self.assertEqual(type(result2), type(first_step_keyboard))
        self.assertEqual(registragion_process, True)

    def test_change_group_step_2_not_in_registragion_process_return_error_message(self):
        result = main.change_group_step_2(222222222, 'Очное обучение')
        self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))

    def test_change_group_step_2_take_correct_data_return_correct(self):
        second_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
        undergraduate = telebot.types.KeyboardButton('Бакалавриат')
        magistracy = telebot.types.KeyboardButton('Магистратура')
        second_step_keyboard.add(undergraduate, magistracy)

        main.change_group_step_1(111111111)
        registragion_process = db_funcs_for_students_db.get_state_of_registragion_process(111111111)
        result1 = main.change_group_step_2(111111111, 'Очное обучение')[0]
        result2 = main.change_group_step_2(111111111, 'Очное обучение')[1]
        
        education_form = db_funcs_for_students_db.get_education_form(111111111)

        self.assertEqual(result1, 'На каком направлении ты учишься?')
        self.assertEqual(type(result2), type(second_step_keyboard))
        self.assertEqual(education_form, 'Очное обучение')
        
    def test_change_group_step_3_not_in_registragion_process_return_error_message(self):
        result = main.change_group_step_3(222222222, 'Очное обучение')
        self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))

    def test_change_group_step_3_take_undergraduate_return_correct(self):
        main.change_group_step_1(111111111)
        
        third_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
        course_1 = telebot.types.KeyboardButton('1 курс')
        course_2 = telebot.types.KeyboardButton('2 курс')
        course_3 = telebot.types.KeyboardButton('3 курс')
        course_4 = telebot.types.KeyboardButton('4 курс')
        third_step_keyboard.add(course_1, course_2, course_3, course_4)

        result1 = main.change_group_step_3(111111111, 'бакалавриат')[0]
        result2 = main.change_group_step_3(111111111, 'бакалавриат')[1]

        academic_degree = db_funcs_for_students_db.get_academic_degree(111111111)

        self.assertEqual(result1, 'На каком курсе ты учишься?')
        self.assertEqual(type(result2), type(third_step_keyboard))
        self.assertEqual(academic_degree, 'бакалавриат')
        
    def test_change_group_step_3_take_magistracy_return_correct(self):
        main.change_group_step_1(111111111)

        third_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
        course_1 = telebot.types.KeyboardButton('1 курс')
        course_2 = telebot.types.KeyboardButton('2 курс')
        third_step_keyboard.add(course_1, course_2)

        result1 = main.change_group_step_3(111111111, 'магистратура')[0]
        result2 = main.change_group_step_3(111111111, 'магистратура')[1]

        academic_degree = db_funcs_for_students_db.get_academic_degree(111111111)

        self.assertEqual(result1, 'На каком курсе ты учишься?')
        self.assertEqual(type(result2), type(third_step_keyboard))
        self.assertEqual(academic_degree, 'магистратура')
        
    def test_change_group_step_4_not_in_registragion_process_return_error_message(self):
        result = main.change_group_step_3(222222222, '1 курс')
        self.assertEqual(result, ('Эта команда доступна только в процессе смены группы', 'main_keyboard'))

    def test_change_group_step_4_take_undergraduate_return_correct(self):
        main.change_group_step_1(111111111)

        fourth_step_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
        first_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag)
        second_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_afk)
        third_timetable = telebot.types.KeyboardButton(texts_for_lesgaft_bot.timetable_mag_tour)

        result1 = main.change_group_step_4(111111111, '1 курс')[0]
        result2 = main.change_group_step_4(111111111, '1 курс')[1]

        number_of_course = db_funcs_for_students_db.get_number_of_course(111111111)

        self.assertEqual(result1, 'Как называется твоё расписание на сайте?')
        self.assertEqual(type(result2), type(fourth_step_keyboard))
        self.assertEqual(number_of_course, 1)

@unittest.skip("passed")    
class Test_site_parser_undergraduate_class(unittest.TestCase):

    try:
        db_funcs_for_site_parser.drop_db()
    except:
        None

    @classmethod
    def setUpClass(cls):
        db_funcs_for_site_parser.create_db()
        db_funcs_for_site_parser.insert_link_to_current_links('zovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_zovs_-_2_sem._20.01.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('lovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._25.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('zovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_kurs_zovs_1.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('lovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_kurs_lovs_19.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('zovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._20.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('lovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_lovs_-_2_sem._19.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('zovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_zovs_19.02.xlsx')
        db_funcs_for_site_parser.insert_link_to_current_links('lovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.03.xlsx')
        
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_site_parser.drop_db()

    def test_return_even_or_odd(self):
        obj = site_parser_class.Site_parser_unergraduate()
        self.assertEqual(obj.return_even_or_odd(1), 'odd')
        self.assertEqual(obj.return_even_or_odd(2), 'even')
        self.assertEqual(obj.return_even_or_odd(5), 'odd')
        self.assertEqual(obj.return_even_or_odd(8), 'even')

    def test_create_html_string(self):
        obj = site_parser_class.Site_parser_unergraduate()
        res_1 = obj.create_html_string(3)
        res_2 = obj.create_html_string(4)
        expect_1 = 'views-row views-row-3 views-row-odd'
        expect_2 = 'views-row views-row-4 views-row-even'
        self.assertEqual(res_1, expect_1)
        self.assertEqual(res_2, expect_2)

    def test_formate_name(self):
        obj = site_parser_class.Site_parser_unergraduate()
        res_1 = obj.formate_name('1_kurs_zovs')
        expect_1 = 'zovs_1_kurs'
        self.assertEqual(res_1, expect_1)

    def test_is_Changed(self):
        obj = site_parser_class.Site_parser_unergraduate()
        res_1 = obj.is_Changed('http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_zovs_-_2_sem._20.01.xlsx')
        res_2 = obj.is_Changed('http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._20.01.xlsx')
        self.assertEqual(res_1, False)
        self.assertEqual(res_2, True)

    def test_find_file_link(self):
        obj = site_parser_class.Site_parser_unergraduate()
        res_1 = obj.find_file_link(texts_for_tests.html_text, 2)
        res_2 = obj.find_file_link(texts_for_tests.html_text, 3)
        expect_1 = 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._20.02.xlsx'
        expect_2 = 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_zovs_-_2_sem._17.02.xlsx'
        self.assertEqual(res_1, expect_1)
        self.assertEqual(res_2, expect_2)

    @patch('requests.get', return_value = texts_for_tests.html_text)
    def test_find_changed_files(self, get):
        obj = site_parser_class.Site_parser_unergraduate()
        res_1 = obj.find_changed_files()
        expect_1 = ['http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_lovs_-_2_sem._20.02.xlsx', 
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_kurs_zovs_-_2_sem._17.02.xlsx', 
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_kurs_zovs_19.02.xlsx', 
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_kurs_zovs_-_2_sem._17.02.xlsx', 
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_kurs_lovs_19.02.xlsx']
        self.assertEqual(res_1, expect_1)

class Test_excel_parser(unittest.TestCase):
    
    conn = sqlite3.connect('subjects.db')
    cursor = conn.cursor()

    def test_format_group_name(self):
        names_from_excel = texts_for_tests.group_names_from_excel
        normal_group_names = texts_for_tests.normal_group_names
        obj = excel_parser.Excel_parser()
        for x in range(len(normal_group_names)):
            normal_name = normal_group_names[x]
            excel_name = names_from_excel[x]
            formatted_name = obj.format_group_name(excel_name)
            self.assertEqual(normal_name, formatted_name)

    def test_run_parser(self):
        # тестируется только бакалавриат очка, потому что метод parse_work_file_using_name
        # использует те же функци и методы и протестирован снизу
        parser = excel_parser.Excel_parser()
        parser.run_parser('test_time_tables/full_time_undergraduate')
        groups_and_expected_number_of_records = {
            'zovs_1_kurs' : 30,
            'zovs_2_kurs' : 32,
            'zovs_3_kurs' : 30,
            'zovs_4_kurs' : 30,
            'lovs_1_kurs' : 30,
            'lovs_2_kurs' : 32,
            'lovs_3_kurs' : 30,
            'lovs_4_kurs' : 30,
        }
        for couple in groups_and_expected_number_of_records:
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            self.assertEqual(expected_number_of_record, actual_number_of_record)

    def test_undergraduate_parser(self):
        parser = excel_parser.Excel_parser()
        groups_and_expected_number_of_records = {
            'zovs_1_kurs' : 30,
            'zovs_2_kurs' : 32,
            'zovs_3_kurs' : 30,
            'zovs_4_kurs' : 30,
            'lovs_1_kurs' : 30,
            'lovs_2_kurs' : 32,
            'lovs_3_kurs' : 30,
            'lovs_4_kurs' : 30,
        }
        for couple in groups_and_expected_number_of_records:
            parser.parse_work_file_using_name(couple, 'test_time_tables/full_time_undergraduate')
            req = f"SELECT COUNT(*) FROM {couple}"
            self.cursor.execute(req)
            expected_number_of_record = self.cursor.fetchall()[0][0]
            actual_number_of_record = groups_and_expected_number_of_records[couple]
            self.assertEqual(expected_number_of_record, actual_number_of_record)


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
            self.assertEqual(expected_number_of_record, actual_number_of_record)


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
            self.assertEqual(expected_number_of_record, actual_number_of_record)


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
            self.assertEqual(expected_number_of_record, actual_number_of_record)

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
            self.assertEqual(expected_number_of_record, actual_number_of_record)



if __name__ == '__main__':
    unittest.main()     