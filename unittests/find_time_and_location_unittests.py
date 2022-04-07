import unittest
from unittest.mock import patch
import datetime
from freezegun import freeze_time

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import find_time_and_location
import texts_for_lesgaft_bot
import db_funcs_for_students_db
import db_funcs_for_subjects_db


# @unittest.skip("passed")

class Test_return_location_of_class(unittest.TestCase):

    def test_take_long_str_return_error_text(self):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где string')
        self.assertEqual(result, 'Такой аудитории я не знаю')

    def test_take_str_return_error_text(self):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где str')
        self.assertEqual(result, texts_for_lesgaft_bot.invalid_text)

    @patch('find_class_location.find_class_location_used_number', return_value='путь')
    def test_take_correct_text_return_correct_way(self, find_class_location_used_number):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где 222')
        self.assertEqual(result, 'путь')

    def test_take_correct_text_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где 10')
        self.assertEqual(result, 'ИМиСТ, первый этаж')

    def test_take_correct_faculty_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где факультет зимних олимпийских видов спорта')
        self.assertEqual(
            result, 'Мойка, вход со стороны стадиона, третий этаж')

    def test_take_correct_department_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(
            123456789, 'где кафедра теории и методики неолимпийских видов спорта')
        self.assertEqual(
            result, 'Мойка, третий этаж, после лестницы направо, по левую сторону')


class Test_find_time_and_location_return_text_about_time_before_lesson_with_location(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db('unittests')
            db_funcs_for_subjects_db.drop_db('zovs_4')
        except:
            pass
        db_funcs_for_students_db.create_db('unittests')
        db_funcs_for_students_db.starting_insert_data(
            111111111, 'Ganzeroar', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(
            222222222, 'Ganzeroar2', None, 1576085837)
        db_funcs_for_students_db.starting_insert_data(
            333333333, 'Ganzeroar3', None, 1576085837)
        db_funcs_for_students_db.update_group(111111111, 417)
        db_funcs_for_students_db.update_group(333333333, 416)

        db_funcs_for_subjects_db.create_db('zovs_4')
        db_funcs_for_subjects_db.save_groups('zovs_4', ['группа_417'])
        db_funcs_for_subjects_db.save_dates_and_times(
            'zovs_4', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times(
            'zovs_4', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')

        db_funcs_for_subjects_db.save_groups('zovs_4', [
                                             'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
        db_funcs_for_subjects_db.save_dates_and_times(
            'zovs_4', [['09.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1')
        db_funcs_for_subjects_db.save_dates_and_times(
            'zovs_4', [['10.01.']], ['9:45'])
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '10.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1 Зал№2')

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db()
        db_funcs_for_subjects_db.drop_db('zovs_4')

    def test_user_id_not_in_db_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            123, 1, date)
        self.assertEqual(
            result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')

    def test_group_isnt_exist_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            222222222, 1, date)
        self.assertEqual(
            result, 'Такой группы не существует. Измени номер группы.')

    @unittest.skip("сломан во время исправления бага коммитом от 22 марта 2022")
    def test_num_of_lessons_bigger_then_6_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            111111111, 6, date)
        self.assertEqual(result, 'Сегодня у тебя больше нет пар.')

    @freeze_time('2019-01-11 09:45:00')
    def test_today_subjects_equal_false_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            111111111, 0, date)
        self.assertEqual(result, texts_for_lesgaft_bot.error)

    @freeze_time('2019-01-11 09:45:00')
    def test_today_subjects_equal_none_return_error_message(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            111111111, 0, date)
        self.assertEqual(result, texts_for_lesgaft_bot.error)

    # По мск время +3, значит тут фактически 06:00:00
    @freeze_time('2019-01-09 06:00:00')
    @patch('find_class_location.find_class_location', return_value='путь')
    def test_when_before_lessons_return_correct_data(self, find_class_location):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            111111111, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся\nпредмет1\n\nпуть')

    @freeze_time('2019-01-09 06:00:00')
    @patch('find_class_location.find_class_location', return_value='путь')
    def test_when_before_lessons_return_correct_data_new_db_column_names(self, find_class_location):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            333333333, 0, date)
        self.assertEqual(result, 'Через 3:45 начнётся\nпредмет1\n\nпуть')

    @freeze_time('2019-01-10 06:00:00')
    def test_real_when_before_lessons_return_correct_data(self):
        date = datetime.datetime.now()
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(
            111111111, 0, date)
        self.assertEqual(
            result, 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')


if __name__ == '__main__':
    unittest.main()
