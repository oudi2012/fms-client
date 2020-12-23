# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidget, QTableView, QHeaderView, QVBoxLayout, QApplication

from src.com.ddky.fms.entry.bill_entry import third_bill_map
from src.com.ddky.fms.jdbc.mysql_dml import querySQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


# 表格样式
def tableStyle():
    style_sheet = """
            QHeaderView::section {
                border: solid dashed dashed solid;
                border-bottom-color: 1px solid #DDDDDD;
                background-color: #F4F4F4;
            }
            QPushButton {
                max-width: 18ex;
                max-height: 6ex;
                font-size: 11px;
            }
            QLineEdit {
                max-width: 30px
            }
        """
    return style_sheet


class TableUtil(QTableWidget):

    def __init__(self, headers, dataList):
        super(TableUtil, self).__init__()
        col_length = 0
        row_length = 0
        if headers is None:
            logging.info("数据表列头标题不能为空")
        else:
            col_length = len(headers)
        if dataList is None:
            logging.info("数据表没有获取到数据")
        else:
            row_length = len(dataList)
        # 根据数据列创建数据表
        self.model = QStandardItemModel(row_length, col_length)
        self.model.setHorizontalHeaderLabels([title for title in headers.values()])
        r_index = 0
        for row in dataList:
            c_index = 0
            for col in headers.keys():
                item_value = str(row[col])
                if row[col] is None:
                    item_value = ''
                elif item_value[0] == 'b':
                    item_value = item_value[2:-1]
                item = QStandardItem(item_value)
                self.model.setItem(r_index, c_index, item)
                c_index = c_index + 1
            r_index = r_index + 1
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        # 水平方向，表格大小扩展到适当的尺寸
        self.tableView.horizontalHeader().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.setStyleSheet(tableStyle())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sql_where = " order by id desc"
    select_sql = querySQLAndWhere("fms_third_bill", ",".join(third_bill_map.keys()), sql_where)
    sql_helper = MySQLHelper()
    result = sql_helper.queryByParam(select_sql, 40)
    table = TableUtil(third_bill_map, result)
    table.show()
    sys.exit(app.exec_())
