import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import texts_for_lesgaft_bot
import request_handler
import db_funcs_for_subjects_db
import db_funcs_for_students_db
import unittest
from freezegun import freeze_time

import os


# @unittest.skip("passed")

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

        # FOR TESTER
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '11.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '11.01.', '9:45', 'группа_417', 'ауд. 28\nИстория ФКиС\nСеминар\nРыбакова О.Б.')
        # FOR TESTER
        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '12.01.', '9:45')

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
        # db_funcs_for_subjects_db.save_date_and_time(
        #    'zovs_4', '10.01.', '9:45')
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

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_students_db.drop_db('unittests')
        db_funcs_for_subjects_db.drop_db('zovs_4')

    @freeze_time('2019-01-10 03:00:00')
    def test_return_where_is_the_lesson_take_correct_data_return_correct(self):
        result = request_handler.return_where_is_the_lesson(111111111)
        self.assertEqual(
            result[0], 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-10 03:00:00')
    def test_main_request_handler_take_where_is_the_lesson_request_return_correct(self):
        result = request_handler.main_request_handler('Где пара?', 111111111)
        self.assertEqual(
            result[0], 'Через 3:45 начнётся\nпредмет1 Зал№2\n\nМанеж, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-09 03:00:00')
    def test_return_today_lessons_take_correct_data_return_correct(self):
        result = request_handler.return_today_lessons(111111111)
        expected_text = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-09 03:00:00')
    def test_main_request_handler_take_today_lessons_request_return_correct(self):
        result = request_handler.main_request_handler(
            'Какие сегодня пары?', 111111111)
        expected_text = 'Расписание на среду (09.01.2019.)\n\n9:45-11:15\nпредмет1\n\n11:30-13:00\nпредмет2\n\n13:30-15:00\nпредмет3\n\n15:15-16:45\nпредмет4\n\n17:00-18:30\nпредмет5\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-10 03:00:00')
    def test_return_tomorrow_lessons_take_correct_data_return_correct(self):
        result = request_handler.return_today_lessons(111111111)
        expected_text = 'Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-09 03:00:00')
    def test_main_request_handler_take_tomorrow_lessons_request_return_correct(self):
        result = request_handler.main_request_handler(
            'Какие завтра пары?', 111111111)
        expected_text = 'Расписание на четверг (10.01.2019.)\n\n9:45-11:15\nпредмет1 Зал№2\n\n'
        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    def test_return_where_is_the_classroom_take_correct_data_return_correct(self):
        result = request_handler.return_where_is_the_classroom(
            111111111, 'где 10')
        self.assertEqual(result[0], 'ИМиСТ, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_where_is_the_classroom_request_return_correct(self):
        result = request_handler.main_request_handler('где 10', 111111111)
        self.assertEqual(result[0], 'ИМиСТ, первый этаж')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_return_to_menu_return_menu(self):
        result = request_handler.main_request_handler(
            'Вернуться в меню', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.go_to_menu_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Расписание'}], [
                         {'text': 'Настройки'}], [{'text': 'Что умеет ЛесгафтБот'}]])

    def test_main_request_handler_take_what_lesgaftbot_can_do_return_text(self):
        result = request_handler.main_request_handler(
            'Что умеет ЛесгафтБот', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.what_lesgaftbot_can_do_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Расписание'}], [
                         {'text': 'Настройки'}], [{'text': 'Что умеет ЛесгафтБот'}]])

    def test_main_request_handler_take_settings_and_user_not_in_news_subscribers_return_settins(self):
        result = request_handler.main_request_handler('Настройки', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[
                         {'text': 'Связь с разработчиком'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_settings_and_user_already_in_news_subscribers_return_correct_settins(self):
        result = request_handler.main_request_handler('Настройки', 222222222)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[
                         {'text': 'Связь с разработчиком'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_go_to_timetables_return_timetables_menu(self):
        result = request_handler.main_request_handler('Расписание', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.go_to_timetables_stage_text)
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_communication_with_developer_return_text(self):
        result = request_handler.main_request_handler(
            'Связь с разработчиком', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.communication_with_developer_text)
        self.assertEqual(result[1].keyboard, [[
                         {'text': 'Связь с разработчиком'}], [{'text': 'Вернуться в меню'}]])

    def test_main_request_handler_take_return_to_settings_return_text(self):
        result = request_handler.main_request_handler(
            'Вернуться в настройки', 111111111)
        self.assertEqual(
            result[0], texts_for_lesgaft_bot.go_to_settings_stage_text)
        self.assertEqual(result[1].keyboard, [[
                         {'text': 'Связь с разработчиком'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-11 03:00:00')
    def test_try_to_find_bug_in_button(self):
        result = request_handler.return_where_is_the_lesson(111111111)
        self.assertEqual(
            result[0], 'Через 3:45 начнётся\nауд. 28\nИстория ФКиС\nСеминар\nРыбакова О.Б.\n\nМойка, второй этаж, налево от охранника, по левую сторону')
        self.assertEqual(result[1].keyboard, [[{'text': 'Где пара?'}], [{'text': 'Какие сегодня пары?'}], [
                         {'text': 'Какие завтра пары?'}], [{'text': 'Вернуться в меню'}]])

    @freeze_time('2019-01-12 03:00:00')
    def test_take_imist_location_return_correct_way(self):
        location = 'ауд. 7 ИМиСТ'
        path_to_location = 'Мойка, третий этаж, от лестницы налево'

        db_funcs_for_subjects_db.save_date_and_time(
            'zovs_4', '12.01.', '9:45')
        db_funcs_for_subjects_db.save_subj(
            'zovs_4', '12.01.', '9:45', 'группа_417', f'{location}\nX')

        result = request_handler.return_where_is_the_lesson(111111111)
        self.assertEqual(
            result[0], f'Через 3:45 начнётся\n{location}\nX\n\n{path_to_location}'
        )


if __name__ == '__main__':
    unittest.main()
