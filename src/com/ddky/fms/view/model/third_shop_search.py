# -*- coding: utf-8 -*-

import logging

from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt5.QtCore import Qt

from src.com.ddky.fms.entry.bill_config import PAGE_SIZE

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# 搜索栏标题的高度
lb_search_height = 25
# 搜索栏输入框的高度
txt_search_height = 25
# 菜单高度
menu_height = 25


# 搜索样式
def searchStyle():
    style_sheet = """
        QFrame#thirdShopSearch {
            border: none;
            border-top: 1px solid #95B8E7;
        }
        QPushButton {
            border: none;
            border-radius:8px;
            background-image:url(images/btn_search.png);
        }
        QPushButton#sync_data {
            border: none;
            border-radius:8px;
            background-image:url(images/reload.png);
        }
        QPushButton#sync_data:hover {
            border:2px solid #95B8E7;
        }
        QPushButton:hover {
            border:2px solid #95B8E7;
        }
        QLineEdit {
            border: 1px solid #95B8E7;
        }
        QLabel {
            border: none;
            max-width: 80px;
        }
    """
    return style_sheet


# 三方搜索框布局
class ThirdShopSearchWidget(QFrame):
    search_sql = {}
    sql_where = ''
    sql_where_value = []

    def __init__(self, crt_menu_name, search_signal):
        super(ThirdShopSearchWidget, self).__init__()
        self.search_sql = {'sql_where': '', 'sql_where_value': ''}
        self.setStyleSheet(searchStyle())
        self.setObjectName("thirdShopSearch")
        self.task_search_layout = QGridLayout()
        self.txt_shop_name = QLineEdit()
        self.txt_shop_id = QLineEdit()
        self.crt_menu_name = crt_menu_name
        self.setFixedHeight(50)
        self.load_search(search_signal)

    # 三方店铺搜索
    def load_search(self, search_signal):
        # 横向间距
        self.task_search_layout.setHorizontalSpacing(5)
        # 纵向间距
        self.task_search_layout.setVerticalSpacing(0)
        lb_shop_name = QLabel(self)
        lb_shop_name.setText("店铺名称：")
        lb_shop_name.setFixedHeight(lb_search_height)
        lb_shop_name.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.task_search_layout.addWidget(lb_shop_name, 0, 0, 1, 1)
        self.txt_shop_name.setObjectName("shop_name")
        self.txt_shop_name.setFixedHeight(txt_search_height)
        self.txt_shop_name.setFixedWidth(200)
        self.task_search_layout.addWidget(self.txt_shop_name, 0, 1, 1, 1)
        # 店铺编号
        lb_shop_id = QLabel(self)
        lb_shop_id.setText("店铺编号：")
        lb_shop_id.setFixedHeight(lb_search_height)
        lb_shop_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.task_search_layout.addWidget(lb_shop_id, 0, 2, 1, 1)
        self.txt_shop_id.setObjectName("shop_id")
        self.txt_shop_id.setFixedHeight(txt_search_height)
        self.txt_shop_id.setFixedWidth(200)
        self.task_search_layout.addWidget(self.txt_shop_id, 0, 3, 1, 1)
        btn_search = QPushButton()
        btn_search.setFixedWidth(menu_height)
        btn_search.setFixedHeight(lb_search_height)
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.clicked.connect(lambda: self.search_param(search_signal))
        self.task_search_layout.addWidget(btn_search, 0, 4, 1, 1)
        sync_data = QPushButton()
        sync_data.setObjectName("sync_data")
        sync_data.setFixedWidth(menu_height)
        sync_data.setFixedHeight(lb_search_height)
        sync_data.setCursor(Qt.PointingHandCursor)
        sync_data.clicked.connect(lambda: self.search_param(search_signal))
        self.task_search_layout.addWidget(sync_data, 0, 5, 1, 4)
        self.task_search_layout.setContentsMargins(1, 1, 0, 0)
        self.setLayout(self.task_search_layout)

    # 三方店铺
    def search_param(self, search_signal):
        self.sql_where = ''
        self.sql_where_value.clear()
        shop_name = self.txt_shop_name.text()
        if shop_name is not None and len(shop_name) > 0:
            self.sql_where += " (name like concat('%%', %s, '%%') or thirdName like concat('%%', %s, '%%') ) "
            self.sql_where_value.append(shop_name)
            self.sql_where_value.append(shop_name)
        shop_id = self.txt_shop_id.text()
        if shop_id is not None and len(shop_id) > 0:
            self.sql_where += " and (thirdShopId=%s or platformId=%s) "
            self.sql_where_value.append(shop_id)
            self.sql_where_value.append(shop_id)
        # 改变表格内容
        self.sql_where = self.sql_where.strip()
        if self.sql_where.startswith('and'):
            self.sql_where = self.sql_where[3:]
        self.sql_where = ' where ' + self.sql_where
        self.search_sql = {'sql_where': self.sql_where, 'sql_where_value': tuple(self.sql_where_value)}
        search_signal.emit({'search_param': self.search_sql, 'pageIndex': 1, 'pageSize': PAGE_SIZE})
