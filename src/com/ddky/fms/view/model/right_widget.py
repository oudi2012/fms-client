# -*- coding: utf-8 -*-

import logging

from PyQt5.QtWidgets import QVBoxLayout, QFrame
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

    def __init__(self, menu_param, menu_signal):
        super(RightWidget, self).__init__()
        self.setObjectName("right_widget")
        self.right_layer = QVBoxLayout()
        menu_signal.connect(self.reload)
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
            search_widget = ThirdShopSearchWidget(menu_param['name'])
            self.right_layer.addWidget(search_widget, 1)
        elif menu_param['name'] == 'btn_excel_path':
            table_widget = PathWidget()
            self.right_layer.addWidget(table_widget, 7)
            return
        elif menu_param['name'] == 'btn_third_bill':
            search_widget = ThirdBillSearchWidget(menu_param['name'])
            self.right_layer.addWidget(search_widget, 1)
        # 创建数据表
        table_widget = TableViewWidget(menu_param['name'])
        self.right_layer.addWidget(table_widget, 7)
        # 创建分页
        page_widget = PageViewWidget()
        self.right_layer.addWidget(page_widget, 1)
        if search_widget is None:
            table_widget.load_data({'sql_where': '', 'sql_where_value': ''}, 1, 30)
        else:
            table_widget.load_data(search_widget.search_sql, 1, 30)


