import unittest
from unittest.mock import patch

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)
import db_funcs_for_site_parser
import site_parser
import texts_for_tests


class Test_site_parser_undergraduate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db_funcs_for_site_parser.drop_db()
        except:
            pass

        db_funcs_for_site_parser.create_db()
        db_funcs_for_site_parser.insert_link_to_current_links()
        db_funcs_for_site_parser.change_link_in_current_links(
            'lovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_lovs_-_2_sem._20.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links(
            'zovs_1_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_zovs_-_2_sem._17.02.xlsx')

        db_funcs_for_site_parser.change_link_in_current_links(
            'zovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_zovs.xls')
        db_funcs_for_site_parser.change_link_in_current_links(
            'lovs_2_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_lovs.xlsx')

        db_funcs_for_site_parser.change_link_in_current_links(
            'zovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_zovs_-_2_sem._20.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links(
            'lovs_3_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_lovs_-_2_sem._19.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links(
            'zovs_4', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_zovs_19.02.xlsx')
        db_funcs_for_site_parser.change_link_in_current_links(
            'lovs_4_kurs', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_lovs_19.03.xlsx')

    @classmethod
    def tearDownClass(cls):
        db_funcs_for_site_parser.drop_db()
    @unittest.skip("broken, outdated")
    def test_is_changed_return_true(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.is_changed(
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_lovs_-_2_sem._25.02.xlsx')
        self.assertEqual(result, True)
    @unittest.skip("broken, outdated")
    def test_is_changed_return_false(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.is_changed(
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//1_lovs_-_2_sem._20.02.xlsx')
        self.assertEqual(result, False)

    @unittest.skip("broken, outdated")
    @patch.object(site_parser.Site_parser, 'is_file_exist')
    def test_find_changed_files_return_4_changed_file_link(self, is_file_exist_mock):
        is_file_exist_mock.return_value = 200
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.find_changed_files(soup_obj)
        self.assertEqual(len(result), 4)
        self.assertEqual(result, ['http://www.lesgaft.spb.ru/sites/default/files//shedul//2_lovs_19.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//2_zovs_19.02.xlsx',
                                  'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_zovs_-_2_sem._17.02.xlsx', 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_lovs_19.02.xlsx'])

    def test_get_file_link_from_site_full_time_undergraduate_return_filelink(self):
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.get_file_link_from_site_full_time_undergraduate(
            7, soup_obj)
        self.assertEqual(
            result, 'http://www.lesgaft.spb.ru/sites/default/files//shedul//3_zovs_-_2_sem._17.02.xlsx')

    def test_find_file_link_return_correct_link(self):
        obj = site_parser.Site_parser_undergraduate()
        soup_obj = obj.get_soup_obj(texts_for_tests.html_text)
        result = obj.find_file_link(8, soup_obj)
        self.assertEqual(
            result, 'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_lovs_19.02.xlsx')

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
        result = obj.get_name_of_course(
            'http://www.lesgaft.spb.ru/sites/default/files//shedul//4_lovs_19.02.xlsx')
        self.assertEqual(result, '4_lovs')

    def test_formate_name_return_correct(self):
        obj = site_parser.Site_parser_undergraduate()
        result = obj.formate_name('3_zovs')
        self.assertEqual(result, 'zovs_3_kurs')

if __name__ == '__main__':
    unittest.main()
