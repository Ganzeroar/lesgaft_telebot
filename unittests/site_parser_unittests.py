import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import texts_for_tests
import site_parser
import unittest


class Test_site_parser_undergraduate(unittest.TestCase):

    def test_get_lovs_link_return_links(self):
        obj = site_parser.Site_parser_undergraduate()
        html_text = texts_for_tests.html_text
        soup_obj = obj.get_soup_obj(html_text)
        result = obj.get_lovs_links(soup_obj)
        expected_result = [
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_lovs_19_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_lovs_14.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_lovs_13_04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_lovs_15_04_0_0.xlsx'
        ]
        self.assertEqual(result, expected_result)

    def test_get_zovs_link_return_links(self):
        obj = site_parser.Site_parser_undergraduate()
        html_text = texts_for_tests.html_text
        soup_obj = obj.get_soup_obj(html_text)
        result = obj.get_zovs_links(soup_obj)
        expected_result = [
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_zovs_13_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_zovs_13.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_zovs_19_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_zovs_15_04_0.xlsx'
        ]
        self.assertEqual(result, expected_result)

    def test_get_all_links_return_links(self):
        obj = site_parser.Site_parser_undergraduate()
        html_text = texts_for_tests.html_text
        soup_obj = obj.get_soup_obj(html_text)
        result = obj.get_all_links(soup_obj)
        expected_result = [
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_lovs_19_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_lovs_14.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_lovs_13_04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_lovs_15_04_0_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_zovs_13_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_zovs_13.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_zovs_19_04.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_zovs_15_04_0.xlsx'
        ]
        self.assertEqual(result, expected_result)


class Test_site_parser_undergraduate_imist(unittest.TestCase):

    def test_get_imist_link_return_links(self):
        obj = site_parser.Site_parser_undergraduate_imist()
        html_text = texts_for_tests.html_text
        soup_obj = obj.get_soup_obj(html_text)
        result = obj.get_imist_links(soup_obj)
        expected_result = [
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_imist_do_30.04_2.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_imist-4-sem-do-30.04-itog_1.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_imist_do_30.04_4_3.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_imist_do_02.074.xlsx'
        ]
        self.assertEqual(result, expected_result)


class Test_site_parser_undergraduate_afk(unittest.TestCase):

    def test_get_afk_link_return_links(self):
        obj = site_parser.Site_parser_undergraduate_afk()
        html_text = texts_for_tests.html_text
        soup_obj = obj.get_soup_obj(html_text)
        result = obj.get_afk_links(soup_obj)
        expected_result = [
            'http://lesgaft.spb.ru/sites/default/files//shedul/1_afk_11.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/2_afk_11.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/3_afk_11.04_0.xlsx',
            'http://lesgaft.spb.ru/sites/default/files//shedul/4_afk_11.04.xlsx'
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
