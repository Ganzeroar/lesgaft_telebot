import unittest
from freezegun import freeze_time

import os

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import db_funcs_for_students_db
import db_funcs_for_subjects_db
import request_handler

class Test_request_handler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_students_db.drop_db('unittests')
            db_funcs_for_subjects_db.drop_db('zovs_4')

            os.remove('wrong_timetables_reports.log')
        except:
            pass
        db_funcs_for_students_db.create_db('unittests')
        db_funcs_for_students_db.starting_insert_data(
            111111111, 'Ganzeroar', None, 1576085837)

        db_funcs_for_students_db.update_group(111111111, 417)

        db_funcs_for_subjects_db.create_db('zovs_4')
        db_funcs_for_subjects_db.save_groups('zovs_4', ['группа_417'])


        ##FOR TESTER
        #db_funcs_for_subjects_db.save_date_and_time(
        #    'zovs_4', '11.01.', '9:45')
        #db_funcs_for_subjects_db.save_subj(
        #    'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')
        ##FOR TESTER
    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db('unittests')
        db_funcs_for_subjects_db.drop_db('zovs_4')

    @freeze_time('2019-01-11 03:00:00')
    def test_test_1(self):
        # Если нет точки после ауд, местоположение не отображается

        location = 'ауд 1'
        path_to_location = 'Мойка, третий этаж, от лестницы налево'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )

    @freeze_time('2019-01-11 03:00:00')
    def test_test_2(self):
        # Если ввести Элективные дисциплины по ФКиС, местоположение аудитории не отображается

        location = 'Элективные дисциплины по ФКиС'
        path_to_location = 'Мойка, третий этаж, от лестницы налево'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )
    
    @freeze_time('2019-01-11 03:00:00')
    def test_test_3(self):
        # Если ввести ауд. 7 ИМиСТ,  отображается Такой адитории я не знаю, предположительно из-за наличия ИМиСТ в строке с аудитоией
        
        location = 'ауд. 7 ИМиСТ'
        path_to_location = 'Мойка, третий этаж, от лестницы налево'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )

    @freeze_time('2019-01-11 03:00:00')
    def test_test_4(self):
        # Если ввести ТиМ ИВС, аудитория не отображается
    
        location = 'ТиМ ИВС'
        path_to_location = 'На кафедре?'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )

    @freeze_time('2019-01-11 03:00:00')
    def test_test_5(self):
        # Если ввести Анатомия, аудитория не отображается
    
        location = 'Анатомия'
        path_to_location = '*местонахождение анатомии*'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )

    @freeze_time('2019-01-11 03:00:00')
    def test_test_6(self):
        # Если ввести ауд. 55, 71, отображается Такой аудитории я не знаю
    
        location = 'ауд. 55, 71'
        path_to_location = 'Кафедра англяза и путь туда?'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        print('*******')
        print(result[0])
        print('*******')        
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )

if __name__ == '__main__':
    unittest.main()
