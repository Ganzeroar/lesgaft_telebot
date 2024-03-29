import sys
sys_path = sys.path[0]
path_to_upper_folder = sys_path[:-10]
path_to_excel_validators = path_to_upper_folder+'\excel_validators'
sys.path.append(path_to_excel_validators)

import unittest
import db_funcs_for_subject_db_unittests
import excel_validator_unittests
import excel_validator_imist_unittests
import excel_validator_lovs_zovs_unittests
import find_class_location_unittests
import find_lessons_at_date_unittests
import find_time_and_location_unittests
import request_handler_unittests
import site_parser_unittests




calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(
    db_funcs_for_subject_db_unittests.Test_db_funcs_for_subjects_db))
calcTestSuite.addTest(unittest.makeSuite(
    find_class_location_unittests.Test_find_class_location_find_class_location))
calcTestSuite.addTest(unittest.makeSuite(
    find_lessons_at_date_unittests.Test_find_lessons_at_date_return_lessons_at_date))
calcTestSuite.addTest(unittest.makeSuite(
    find_time_and_location_unittests.Test_return_location_of_class))
calcTestSuite.addTest(unittest.makeSuite(
    find_time_and_location_unittests.Test_find_time_and_location_return_text_about_time_before_lesson_with_location))
calcTestSuite.addTest(unittest.makeSuite(
    request_handler_unittests.Test_request_handler))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_file_name))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_worksheet_names))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_group_struct))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_structure))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_practice_cell))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_imist_unittests.Test_check_cells_with_lessons))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_lovs_zovs_unittests.Test_check_file_name))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_lovs_zovs_unittests.Test_check_worksheet_names))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_lovs_zovs_unittests.Test_check_group_struct))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_lovs_zovs_unittests.Test_check_structure))
calcTestSuite.addTest(unittest.makeSuite(
    site_parser_unittests.Test_site_parser_undergraduate))
calcTestSuite.addTest(unittest.makeSuite(
    site_parser_unittests.Test_site_parser_undergraduate_imist))
calcTestSuite.addTest(unittest.makeSuite(
    site_parser_unittests.Test_site_parser_undergraduate_afk))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_unittests.Test_excel_validator))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_unittests.Test_check_worksheet_name))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_unittests.Test_check_date_struct))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_unittests.Test_check_day_struct))
calcTestSuite.addTest(unittest.makeSuite(
    excel_validator_unittests.Test_check_time_struct))


runner = unittest.TextTestRunner(verbosity=1)

if __name__ == '__main__':
    runner.run(calcTestSuite)
