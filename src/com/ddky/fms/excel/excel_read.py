# coding='utf-8'

import xlrd
import numpy


# 获取excel 数据表中的数据
def excel_list(excel_name, sheet_index=0):
    """ Read Excel with xlrd """
    TC_workbook = xlrd.open_workbook(excel_name)
    sheet = TC_workbook.sheet_by_index(sheet_index)
    return sheet.nrows


def read_excel_xlrd():
    """ Read Excel with xlrd """
    # file
    TC_workbook = xlrd.open_workbook("wm.xlsx")

    # sheet
    all_sheets_list = TC_workbook.sheet_names()
    print("All sheets name in File:", all_sheets_list)

    first_sheet = TC_workbook.sheet_by_index(0)
    print("First sheet Name:", first_sheet.name)
    print("First sheet Rows:", first_sheet.nrows)
    print("First sheet Cols:", first_sheet.ncols)

    first_row = first_sheet.row_values(0)
    print("First row:", first_row)
    first_col = numpy.array(first_sheet.col_values(0), int)
    first_add = first_col + first_col
    print("First Column: ", first_add)

    # cell
    """ cell_value = first_sheet.cell(1, 0).value
   print("The 1th method to get Cell value of row 2 & col 1:", cell_value)
   cell_value2 = first_sheet.row(1)[0].value
   print("The 1th method to get Cell value of row 2 & col 1:", cell_value2)
   cell_value3 = first_sheet.col(0)[1].value
   print("The 3th method to get Cell value of row 2 & col 1:", cell_value3)"""
