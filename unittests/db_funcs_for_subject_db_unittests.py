import unittest
from freezegun import freeze_time
import os

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import db_funcs_for_subjects_db
import db_funcs_for_students_db



class Test_db_funcs_for_subjects_db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db('unittests')
            db_funcs_for_subjects_db.drop_db('zovs_4')

            os.remove('wrong_timetables_reports.log')
        except:
            pass

        db_funcs_for_subjects_db.create_db('zovs_4')
        db_funcs_for_subjects_db.save_groups('zovs_4', ['группа_417'])
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
        db_funcs_for_subjects_db.save_groups('zovs_4', [
                                             'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416'])
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

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db('unittests')
        db_funcs_for_subjects_db.drop_db('zovs_4')

    @freeze_time('2019-01-10 03:00:00')
    def test_get_db_name_take_correct_return_correct(self):
        result = db_funcs_for_subjects_db.get_db_name('группа_417')
        self.assertEqual(result, 'zovs_4')

        result = db_funcs_for_subjects_db.get_db_name(
            'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416')
        self.assertEqual(result, 'zovs_4')

    def test_isgroup_exist(self):
        result = db_funcs_for_subjects_db.is_group_exist(
            'группа_417', 'zovs_4')
        self.assertTrue(result)

        result = db_funcs_for_subjects_db.is_group_exist(
            'группа_416', 'zovs_4')
        self.assertTrue(result)

    def test_return_new_group_name(self):
        result = db_funcs_for_subjects_db.return_new_group_name(
            'группа_416', 'zovs_4')
        self.assertEqual(
            result, 'конькобежный_спорт_фигурное_катание_скалолазание_керлинг_группа_416')

if __name__ == '__main__':
    unittest.main()
