import unittest
import telebot
from unittest.mock import patch
from freezegun import freeze_time
import datetime

import find_time_and_location
import find_lessons_at_date
import find_class_location
import main


import texts_for_lesgaft_bot
import db_funcs_for_students_db
import db_funcs_for_subjects_db

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

if __name__ == '__main__':
    unittest.main()