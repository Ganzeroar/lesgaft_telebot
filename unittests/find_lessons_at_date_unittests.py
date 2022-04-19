import unittest
from freezegun import freeze_time
import datetime


import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import db_funcs_for_students_db
import db_funcs_for_subjects_db
import find_lessons_at_date



class Test_find_lessons_at_date_return_lessons_at_date(unittest.TestCase):

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
        db_funcs_for_subjects_db.save_groups('zovs_4', [
                                             'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.01.', '17:00')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '10.01.', '9:45', 'группа_417', 'предмет1 Зал№2')

        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '11:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет2')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '13:30', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет3')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '15:15', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет4')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.01.', '17:00', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет5')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '10.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '10.01.', '9:45', 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416', 'предмет1 Зал№2')

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.01.', '18:40')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '09.12.', '9:45')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '10.12.', '11:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.12.', '13:30')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '12.12.', '15:15')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '13.12.', '17:00')
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '14.12.', '18:40')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '9:45', 'группа_417', 'предмет1')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '11:30', 'группа_417', 'предмет2')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '13:30', 'группа_417', 'предмет3')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '15:15', 'группа_417', 'предмет4')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '17:00', 'группа_417', 'предмет5')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.01.', '18:40', 'группа_417', 'предмет6')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '09.12.', '9:45', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '10.12.', '11:30', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.12.', '13:30', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '12.12.', '15:15', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '13.12.', '17:00', 'группа_417', 'нет предмета')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '14.12.', '18:40', 'группа_417', 'нет предмета')

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db('unittests')
        db_funcs_for_subjects_db.drop_db('zovs_4')

    @freeze_time('2019-12-22 03:00:00')
    def test_get_sunday_return_sunday_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, date)
        self.assertEqual(result, 'Воскресенье, не учимся!')

    @freeze_time('2019-12-20 03:00:00')
    def test_user_not_in_bd_return_error_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(123, date)
        self.assertEqual(
            result, 'Тебя ещё нет в моей базе данных. Сначала зарегистрируйся.')

    @freeze_time('2019-12-20 03:00:00')
    def test_group_not_exist_return_error_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(222222222, date)
        self.assertEqual(
            result, 'Такой группы не существует. Измени номер группы.')

    @freeze_time('2019-01-09 03:00:00')
    def test_5_subject_all_correct_return_correct_message(self):
        date = datetime.datetime.now()
        result = find_lessons_at_date.return_lessons_at_date(111111111, date)
        expected_string = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result, expected_string)

    @freeze_time('2019-01-09 03:00:00')
    def test_new_db_column_names_return_correct_message(self):
        # тест для проверки новых имён столбиков в базе
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

if __name__ == '__main__':
    unittest.main()
