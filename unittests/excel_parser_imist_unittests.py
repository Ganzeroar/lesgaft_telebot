import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)
path_to_excel_validators = path_to_upper_folder+'\excel_validators\\'
sys.path.append(path_to_excel_validators)

import excel_validator
import excel_parser_imist
import unittest


class Test_get_groups_name(unittest.TestCase):

    def test_take_correct_name_return_file_name_ok(self):
        constants = {
            'number_of_groups': 3,
            'first_group_number': 'Группа 128-М',
            'second_group_number': 'Группа 129-МО',
            'third_group_number': 'Группа 130-Жур',
        }
        obj = excel_parser_imist.Excel_parser_imist()
        result = obj.get_groups_name(constants)
        self.assertEqual('Имя файла ОК\n', result)

    def test_take_incorrect_name_return_error_with_correct_text(self):
        obj = excel_parser_imist.Excel_parser_imist()
        with self.assertRaises(excel_validator.File_not_valid) as context:
            obj.check_file_name('1_imst')
        self.assertEqual('Ошибка в имени файла 1_imst', str(context.exception))
