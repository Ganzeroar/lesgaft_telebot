import unittest
from unittest.mock import patch
from freezegun import freeze_time
import datetime

import find_time_and_location
import texts_for_lesgaft_bot

import find_lessons_at_date

import excel_parser


class Test_find_time_and_location(unittest.TestCase):

    def test_return_location_of_class_take_long_str(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где string')
        self.assertEqual(result, 'Такой аудитории я не знаю')
    def test_return_location_of_class_take_str(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где str')
        self.assertEqual(result, texts_for_lesgaft_bot.invalid_text)
    @patch('find_class_location.find_class_location_used_number', return_value = 'путь')
    def test_return_location_of_class_take_current_text(self, find_class_location_used_number):
        result = find_time_and_location.return_location_of_class(123456789, 'где 222')
        self.assertEqual(result, 'путь')
    def test_return_location_of_class_take_current_text_return_real_answer(self):
        result = find_time_and_location.return_location_of_class(123456789, 'где 10')
        self.assertEqual(result, 'ИЭиСТ, первый этаж')

    @patch('db_funcs_for_students_db.get_group_number', return_value = False)
    def test_return_text_about_time_before_lesson_with_location_user_id_not_in_db(self, get_group_number):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 1)
        self.assertEqual(result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = None)
    def test_return_text_about_time_before_lesson_with_location_group_isnt_exist(self, get_group_number, get_db_name):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 1)
        self.assertEqual(result, 'Такой группы не существует. Измени номер группы.')
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'group_name')
    def test_return_text_about_time_before_lesson_with_location_num_of_lessons_bigger_then_5(self, get_group_number, get_db_name):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 6)
        self.assertEqual(result, 'Сегодня у тебя больше нет пар.')
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'group_name')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = '')
    def test_return_text_about_time_before_lesson_with_location_today_subjects_equal_false(self, get_group_number, get_db_name, get_subjects_today):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 0)
        self.assertEqual(result, texts_for_lesgaft_bot.error)
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'group_name')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = [[None]])
    def test_return_text_about_time_before_lesson_with_location_today_subjects_equal_none(self, get_group_number, get_db_name, get_subjects_today):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 0)
        self.assertEqual(result, texts_for_lesgaft_bot.error)
    # По мск время +3, значит тут фактически 06:00:00    
    @freeze_time('2019-09-24 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'group_name')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = [['Предмет1']])
    @patch('find_class_location.find_class_location', return_value = 'путь')
    def test_return_text_about_time_before_lesson_with_location_before(self, get_group_number, get_db_name, get_subjects_today, find_class_location):
        result = find_time_and_location.return_text_about_time_before_lesson_with_location(123, 0)
        self.assertEqual(result, 'Через 3:45 начнётся Предмет1\n\nпуть')
    
class Test_find_lessons_at_date(unittest.TestCase):
    @freeze_time('2019-12-22 03:00:00')
    def test_return_lessons_at_date_get_sunday(self):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        self.assertEqual(result, 'Завтра воскресенье, не учимся!')
    @freeze_time('2019-12-20 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = False)
    def test_return_lessons_at_date_user_not_in_bd(self, get_group_number):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        self.assertEqual(result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')
    @freeze_time('2019-12-20 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = True)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = None)
    def test_return_lessons_at_date_group_not_exist(self, get_group_number, get_db_name):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        self.assertEqual(result, 'Твоей группы не существует. Измени номер группы.')
    @freeze_time('2019-12-20 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = 111)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'lovs_1_kurs')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = False)
    def test_return_lessons_at_date_subject_not_exist(self, get_group_number, get_db_name, get_subjects_today):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        self.assertEqual(result, 'Твоей группы не существует. Измени номер группы.')
    @freeze_time('2019-12-20 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = 111)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'lovs_1_kurs')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = [['subject1'],['subject2'],['subject3'],['subject4'],['subject5']])
    def test_return_lessons_at_date_subject_all_correct(self, get_group_number, get_db_name, get_subjects_today):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        expected_string = 'Расписание на пятницу (20.12.2019.)\n\n9:45-11:15\nsubject1\n\n11:30-13:00\nsubject2\n\n13:30-15:00\nsubject3\n\n15:15-16:45\nsubject4\n\n17:00-18:30\nsubject5\n\n'
        self.assertEqual(result, expected_string)
    @freeze_time('2019-12-20 03:00:00')
    @patch('db_funcs_for_students_db.get_group_number', return_value = 111)
    @patch('db_funcs_for_subjects_db.get_db_name', return_value = 'lovs_1_kurs')
    @patch('db_funcs_for_subjects_db.get_subjects_today', return_value = [['subject1']])
    def test_return_lessons_at_date_subject_error_with_subj(self, get_group_number, get_db_name, get_subjects_today):
        time_now = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, time_now)
        self.assertEqual(result, texts_for_lesgaft_bot.error)

class Text_excel_parser(unittest.TestCase):

    @patch('work_sheet.cell', return_value = 'Группа 111.')
    def test_return_full_data_of_day(self, return_db_name, create_db):
        result = excel_parser.return_full_data_of_day()
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()