# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QFrame

from src.com.ddky.fms.entry.bill_config import PAGE_SIZE
from src.com.ddky.fms.view.model.crumb_widget import CrumbWidget
from src.com.ddky.fms.view.model.page_view import PageViewWidget
from src.com.ddky.fms.view.model.path_setting import PathWidget
from src.com.ddky.fms.view.model.table_view import TableViewWidget
from src.com.ddky.fms.view.model.third_bill_search import ThirdBillSearchWidget
from src.com.ddky.fms.view.model.third_shop_search import ThirdShopSearchWidget

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# sql 标题高度
lb_sql_height = 25


# 面包屑样式
def rightStyle():
    style_sheet = """
        #right_widget {
            border: 1px solid #95B8E7;
        }
        QLabel {
            border: none;
        }
    """
    return style_sheet


# 右侧布局
class RightWidget(QFrame):
    # 搜索信号
    search_signal = pyqtSignal(dict)
    # page_signal 分页信号
    page_signal = pyqtSignal(list)

    def __init__(self, menu_param, menu_signal):
        super(RightWidget, self).__init__()
        self.setObjectName("right_widget")
        self.right_layer = QVBoxLayout()
        self.search_sql = {'sql_where': '', 'sql_where_value': ''}
        menu_signal.connect(self.reload)
        self.page_signal.connect(self.pageReload)
        self.setLayout(self.right_layer)
        self.setStyleSheet(rightStyle())
        self.loadWidget(menu_param)

    def reload(self, menu_signal):
        menu_param = {'name': menu_signal['name'], 'title': menu_signal['title']}
        for idx in range(self.right_layer.count()):
            self.right_layer.itemAt(idx).widget().deleteLater()
        self.loadWidget(menu_param)

    def loadWidget(self, menu_param):
        self.right_layer.setContentsMargins(0, 0, 0, 0)
        self.right_layer.setSpacing(0)
        # 创建面包屑
        crumb_widget = CrumbWidget(menu_param)
        self.right_layer.addWidget(crumb_widget, 1)
        # 创建搜索框
        search_widget = None
        if menu_param['name'] == 'btn_third_shop':
            search_widget = ThirdShopSearchWidget(menu_param['name'], self.search_signal)
            self.right_layer.addWidget(search_widget, 1)
        elif menu_param['name'] == 'btn_excel_path':
            table_widget = PathWidget()
            self.right_layer.addWidget(table_widget, 7)
            return
        elif menu_param['name'] == 'btn_third_bill':
            search_widget = ThirdBillSearchWidget(menu_param['name'], self.search_signal)
            self.right_layer.addWidget(search_widget, 1)
        # 创建数据表
        self.table_widget = TableViewWidget(menu_param['name'], self.search_signal)
        self.right_layer.addWidget(self.table_widget, 7)
        # 创建分页
        self.page_widget = PageViewWidget(self.page_signal)
        self.right_layer.addWidget(self.page_widget, 1)
        if search_widget is None:
            pageInfo = self.table_widget.load_data({'sql_where': '', 'sql_where_value': ''}, 1, PAGE_SIZE)
        else:
            self.search_sql = search_widget.search_sql
            pageInfo = self.table_widget.load_data(self.search_sql, 1, PAGE_SIZE)
        self.page_widget.curtPage.setText(str(pageInfo['pageIndex']))
        self.page_widget.totalPage.setText('共' + str(pageInfo['pages']) + '页')
        self.page_widget.pageSize.setText('每页显示' + str(PAGE_SIZE) + '条')

    def pageReload(self, page_signal):
        pageInfo = self.table_widget.load_data(self.search_sql, int(page_signal[0]), int(page_signal[1]))
        self.page_widget.curtPage.setText(str(pageInfo['pageIndex']))
        self.page_widget.totalPage.setText('共' + str(pageInfo['pages']) + '页')
        self.page_widget.pageSize.setText('每页显示' + str(PAGE_SIZE) + '条')
