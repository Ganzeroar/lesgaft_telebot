import unittest
from openpyxl import Workbook, load_workbook, utils
import glob

import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
sys.path.append(path_to_upper_folder)
path_to_excel_validators = path_to_upper_folder+'\excel_validators\\'
sys.path.append(path_to_excel_validators)
import main


#class Test_excel_validator(unittest.TestCase):
#    # потенциально валидировать имя файла + 
#    # валидировать количество групп в расписании?
#    # валидировать на поиск пустых строк?
#    # ограничить количество групп в каждом расписании, тем самым контроллируя строки?
#    # провверять правильность день дата время?
#    # проверять первую ячейку по константам на None
#    # добавить поиск пар в 18:40
#    @unittest.skip("passed")
#    def test_take_one_correct_and_one_incorrect_sheetname_return_correct_message(self):
#        obj = excel_validator.Excel_validator()
#        result = obj.run_validator('test_time_tables/full_time_undergraduate')
#        self.assertEqual('Имя файла ОК\nИмена листов ОК\nЛист 21.03. - 26.03.\nСтруктура групп ОК\nСруктура дат ОК\nСруктура дней ОК\nСруктура времени ОК\nЛист 21.03. - 26.03.\nИмена групп ОК\nДаты ОК\nИмена дней ОК\nВремя ОК\n', result)
#
#    #def test_take_full_file_return_correct_message(self):
#    #    obj = excel_validator.Excel_validator()
#    #    result = obj.run_validator('test_time_tables/full_time_undergraduate/fulltest')
#    #    self.assertEqual('ОК\n', result)
