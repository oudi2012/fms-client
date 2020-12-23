# coding='utf-8'

import xlrd
import xlwt
from datetime import datetime
from xlutils.copy import copy


def set_style(front_name, front_height, bold=False):
    style = xlwt.XFStyle()

    front = xlwt.Font()
    front.name = front_name
    front_height = front_height
    front.bold = bold
    front.colour_index = 4

    borders = xlwt.Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    style.font = front
    style.borders = borders
    return style


def write_to_excel():
    """ Write content to a new excel """
    new_workbook = xlwt.Workbook()
    new_sheet = new_workbook.add_sheet("SheetName_test")
    new_sheet.write(0, 0, "hello")
    # write cell with style
    new_sheet.write(0, 1, "world", set_style("Times New Roman", 220, True))

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', '#,##0.00')
    style1 = xlwt.easyxf('D-MM-YY')
    new_sheet.write(1, 0, 1234.56, style0)
    new_sheet.write(1, 1, datetime.now(), style1)

    # write cell with formula
    new_sheet.write(2, 0, 5)
    new_sheet.write(2, 1, 8)
    new_sheet.write(3, 0, xlwt.Formula("A3+B3"))

    new_workbook.save("NewCreateWorkBook.xls")


def write_to_existed_file():
    """ Write content to existed excel file with xlrd """
    rd = xlrd.open_workbook("NewCreateWorkbook.xls", True)

    wd = copy(rd)
    ws = wd.get_sheet(0)

    font = xlwt.Font()
    font.name = "Times New Roman"
    font.height = 220
    font.bold = False

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 2

    cell_style = xlwt.XFStyle()
    cell_style.font = font
    cell_style.borders = borders
    cell_style.pattern = pattern

    ws.write(6, 7, "hello world", cell_style)
    wd.save("NewCreateWorkbook.xls")


if __name__ == '__main__':
    write_to_existed_file()
    print('写入成功')
