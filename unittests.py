import unittest
from unittest.mock import patch
from freezegun import freeze_time
import datetime

import find_time_and_location
import texts_for_lesgaft_bot
import db_funcs_for_students_db
import db_funcs_for_subjects_db

import find_lessons_at_date

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
        
class Test_find_time_and_location_return_text_about_time_before_lesson_with_location(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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
    

class Test_find_lessons_at_date_return_lessons_at_date(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

if __name__ == '__main__':
    unittest.main()