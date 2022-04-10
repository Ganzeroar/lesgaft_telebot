import unittest

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)

import find_class_location

class Test_find_class_location_find_class_location(unittest.TestCase):

    def test_take_correct_data_return_correct_data(self):
        result = find_class_location.find_class_location(
            'ауд. 426\nЛекция Дисциплина по выбору')
        self.assertEqual(
            result, 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону')

    def test_take_real_correct_data_return_correct_data(self):
        real_data = '''ауд. 421\nЛекция\nДисциплина по выбору'''
        result = find_class_location.find_class_location(real_data)
        self.assertEqual(
            result, 'Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону')

if __name__ == '__main__':
    unittest.main()
