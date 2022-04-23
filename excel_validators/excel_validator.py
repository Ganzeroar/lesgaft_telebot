import re

from file_not_valid_exception import File_not_valid
from excel_handler import Excel_handler


class Excel_validator(Excel_handler):

    def check_worksheet_names(self, worksheet_names):
        for worksheet_name in worksheet_names:
            if self.is_reason_to_skip(worksheet_name) == True:
                continue
            result = re.fullmatch(
                r'\d{2}[.]\d{2}[.]\s[-]\s\d{2}[.]\d{2}[.]', worksheet_name)
            if result == None:
                raise File_not_valid(
                    f'Ошибка в имени листа {worksheet_name}\n')
        return 'Имена листов ОК\n'

    def check_day_struct(self, worksheet, file_name, worksheet_name):
        constants = self.return_current_file_constants(file_name)
        const_day_column = constants['day_column']
        const_first_day_row = constants['first_day_row']
        const_last_day_row = constants['last_day_row']

        for row in range(const_first_day_row, const_last_day_row + 1):
            viewed_date_cell = worksheet.cell(row=row, column=const_day_column)
            if self.is_merged(worksheet, viewed_date_cell):
                viewed_day_value = self.get_merged_cell_value(
                    worksheet, viewed_date_cell)
                result = re.fullmatch(r'[А-Я][а-я][.]', viewed_day_value)
                if result == None:
                    raise File_not_valid(
                        f'Ошибка в структуре дня в {viewed_date_cell.coordinate} в листе {worksheet_name}')
            else:
                raise File_not_valid(
                    f'Ошибка в структуре дня в {viewed_date_cell.coordinate} в листе {worksheet_name}')

    def check_date_struct(self, worksheet, work_file_name, worksheet_name):
        constants = self.return_current_file_constants(work_file_name)
        const_date_column = constants['date_column']
        const_first_date_row = constants['first_date_row']
        const_last_date_row = constants['last_date_row']
        for row in range(const_first_date_row, const_last_date_row + 1):
            viewed_date_cell = worksheet.cell(
                row=row, column=const_date_column)
            if self.is_merged(worksheet, viewed_date_cell):
                viewed_date_value = self.get_merged_cell_value(
                    worksheet, viewed_date_cell)
                result = re.fullmatch(r'\d{2}[.]\d{2}[.]', viewed_date_value)
                if result == None:
                    raise File_not_valid(
                        f'Ошибка в структуре даты в {viewed_date_cell.coordinate} в листе {worksheet_name}')
            else:
                raise File_not_valid(
                    f'Ошибка в структуре даты в {viewed_date_cell.coordinate} в листе {worksheet_name}')

    def check_time_struct(self, worksheet, work_file_name, worksheet_name):
        constants = self.return_current_file_constants(work_file_name)
        const_time_column = constants['time_column']
        const_first_time_row = constants['first_time_row']
        const_last_time_row = constants['last_time_row']

        for row in range(const_first_time_row, const_last_time_row + 1):
            viewed_time_cell = worksheet.cell(
                row=row, column=const_time_column)
            if self.is_merged(worksheet, viewed_time_cell):
                raise File_not_valid(
                    f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            else:
                if viewed_time_cell.value == None:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
                result = re.fullmatch(
                    r'\d{1,2}[:]\d{2}', viewed_time_cell.value)
                if result == None:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')

        for row in range(const_first_time_row, const_last_time_row):
            viewed_time_cell = worksheet.cell(
                row=row, column=const_time_column)
            next_viewed_time_cell = worksheet.cell(
                row=row + 1, column=const_time_column)
            viewed_time_value = viewed_time_cell.value
            next_viewed_time_value = next_viewed_time_cell.value
            if viewed_time_value == '9:45':
                if next_viewed_time_value == '11:30':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            elif viewed_time_value == '11:30':
                if next_viewed_time_value == '13:30':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            elif viewed_time_value == '13:30':
                if next_viewed_time_value == '15:15':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            elif viewed_time_value == '15:15':
                if next_viewed_time_value == '17:00':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            elif viewed_time_value == '17:00':
                if next_viewed_time_value == '9:45':
                    continue
                elif next_viewed_time_value == '18:40':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
            elif viewed_time_value == '18:40':
                if next_viewed_time_value == '9:45':
                    continue
                else:
                    raise File_not_valid(
                        f'Ошибка в структуре времени в {viewed_time_cell.coordinate} в листе {worksheet_name}')
