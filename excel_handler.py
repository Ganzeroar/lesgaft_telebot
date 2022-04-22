import configurations

class Excel_handler():

    def is_reason_to_skip(self, worksheet_name):
        worksheet_name = worksheet_name.lower()
        if worksheet_name.lower() in configurations.words_to_skip:
            return True
        month_to_skip = configurations.month_to_skip
        month = worksheet_name[-3:-1]
        if month in month_to_skip:
            return True
        return False

    def is_merged(self, worksheet, viewed_cell):
        for mergedCell in worksheet.merged_cells.ranges:
            if (viewed_cell.coordinate in mergedCell):
                return True
        return False

    def get_merged_cell_value(self, worksheet, cell):
        rng = []
        for s in worksheet.merged_cells.ranges:
            if cell.coordinate in s:
                rng.append(s)
        cell_value = worksheet.cell(rng[0].min_row, rng[0].min_col).value
        return cell_value
    