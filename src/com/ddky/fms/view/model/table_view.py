# -*- coding: utf-8 -*-

import logging

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QHeaderView, QFrame, QHBoxLayout

# 表格样式
from src.com.ddky.fms.entry.menu_table_param import param_menu_table
from src.com.ddky.fms.entry.value_format import format_value
from src.com.ddky.fms.jdbc.mysql_dml import totalSQLAndWhere, querySQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper

# 默认单页显示数据条数
default_page_size = 30


def tableStyle():
    style_sheet = """
        QFrame {
            border: none;
            border-top: 1px solid #95B8E7;
            border-bottom: 1px solid #95B8E7;
        }
        QHeaderView {
            border: none;
        }
        QTableView {
            border: none;
        }
        QHeaderView#hHeader::section {
            background-color: #F5F5F5;
            border: none;
            height: 30;
            text-align: center;
            border-right: 1px solid #95B8E7;
            border-bottom: 1px solid #95B8E7;
        }
        QFrame#task_label {
            background-color: #ffffff;
            border: none;
            height: 30;
            text-align: center;
        }
        QTableView::item:hover {
            background-color: rgba(200,200,220,255);
        }
    """
    return style_sheet


# 分页计算
def page_info(pageIndex, pageSize, totalCount):
    if pageIndex is None or pageIndex <= 0:
        pageIndex = 1
    if pageSize is None or pageSize <= 0:
        pageSize = default_page_size
    if totalCount is None:
        totalCount = 0
    pages = totalCount / pageSize
    more = totalCount % pageSize
    if more > 0:
        pages = pages + 1
    if pages <= 0:
        pages = 1
    if pageIndex >= pages:
        pageIndex = pages
    start = (pageIndex - 1) * pageSize
    return {'pageIndex': int(pageIndex), 'pageSize': int(pageSize), 'totalCount': int(totalCount),
            'pages': int(pages), 'start': int(start)}


# 表格数据显示
class TableViewWidget(QFrame):
    # search_signal 搜索信号
    # page_signal 分页信号
    def __init__(self, crt_menu_name):
        super(TableViewWidget, self).__init__()
        self.setStyleSheet(tableStyle())
        table_layout = QHBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.crt_menu_name = crt_menu_name
        self.tableView = QTableView()
        # 水平方向，表格大小扩展到适当的尺寸
        self.tableView.horizontalHeader().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setObjectName("hHeader")
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setStyleSheet(tableStyle())
        table_layout.addWidget(self.tableView)
        self.setLayout(table_layout)
        defaultParam = param_menu_table[self.crt_menu_name]
        self.fill_table(defaultParam['entry_map'], [defaultParam['default_value']])

    # 右侧内容
    def fill_table(self, headers, dataList):
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
        model = QStandardItemModel(row_length, col_length)
        model.setHorizontalHeaderLabels([title.split('|')[0] for title in headers.values()])
        r_index = 0
        for row in dataList:
            c_index = 0
            for key, value in headers.items():
                arr_val = value.split('|')
                if key not in row.keys() or row[key] is None:
                    item_value = ''
                else:
                    item_value = str(row[key])
                if len(item_value) > 0 and item_value[0] == 'b':
                    item_value = item_value[2:-1]
                item_value = format_value(arr_val[1], item_value)
                item = QStandardItem(item_value)
                model.setItem(r_index, c_index, item)
                c_index = c_index + 1
            r_index = r_index + 1
        self.tableView.setModel(model)

    # 三方店铺数据
    def load_data(self, search_param, pageIndex, pageSize):
        # 根据按钮名称获取默认参数
        sql_helper = MySQLHelper()
        defaultParam = param_menu_table[self.crt_menu_name]
        # 获取总量
        count_sql = totalSQLAndWhere(str(defaultParam['table_name']), search_param['sql_where'])
        if len(search_param['sql_where_value']) > 0:
            totalInfo = sql_helper.findOne(count_sql, search_param['sql_where_value'])
        else:
            totalInfo = sql_helper.findOne(count_sql)
        # 设置页码
        pageInfo = page_info(pageIndex, pageSize, int(totalInfo['total']))
        # 获取具体数据
        sql_order = " order by id desc"
        select_sql = querySQLAndWhere(str(defaultParam['table_name']),
                                      ",".join(defaultParam['entry_map'].keys()), search_param['sql_where'],
                                      sql_order, pageInfo['start'], pageSize)
        if len(search_param['sql_where_value']) > 0:
            result = sql_helper.queryByParam(select_sql, pageSize, search_param['sql_where_value'])
        else:
            result = sql_helper.queryByParam(select_sql, pageSize)
        sql_helper.dispose()
        if len(result) <= 0:
            result.append(defaultParam['default_value'])
        self.fill_table(defaultParam['entry_map'], result)
