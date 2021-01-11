# -*- coding: utf-8 -*-

import logging

from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal

from src.com.ddky.fms.entry.bill_config import PAGE_SIZE
from src.com.ddky.fms.entry.pay_type_enum import page_type

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
        QFrame#thirdBillSearch {
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
class ThirdBillSearchWidget(QFrame):
    search_sql = {}
    sql_where = ''
    sql_where_value = []

    def __init__(self, crt_menu_name, search_signal):
        super(ThirdBillSearchWidget, self).__init__()
        self.time_import_date_start = QDateTimeEdit(QDateTime.currentDateTime())
        self.txt_third_orderId = QLineEdit()
        self.combo_account_type = QComboBox()
        self.combo_pay_type = QComboBox()
        self.time_receive_date_end = QDateTimeEdit(QDateTime.currentDateTime().addDays(3))
        self.time_receive_date_start = QDateTimeEdit(QDateTime.currentDateTime().addDays(3))
        self.time_import_date_end = QDateTimeEdit(QDateTime.currentDateTime())
        self.search_sql = {'sql_where': '', 'sql_where_value': ''}
        self.setStyleSheet(searchStyle())
        self.setObjectName("thirdBillSearch")
        self.search_layout = QGridLayout()
        # 横向间距
        self.search_layout.setHorizontalSpacing(5)
        # 纵向间距
        self.search_layout.setVerticalSpacing(0)
        self.setLayout(self.search_layout)
        self.crt_menu_name = crt_menu_name
        self.setFixedHeight(50)
        self.load_search(search_signal)

    # 三方店铺搜索
    def load_search(self, search_signal):
        lb_third_orderId = QLabel()
        lb_third_orderId.setText("三方单号：")
        lb_third_orderId.setFixedHeight(lb_search_height)
        lb_third_orderId.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_third_orderId, 0, 0, 1, 1)
        self.txt_third_orderId.setObjectName("third_orderId")
        self.txt_third_orderId.setFixedHeight(txt_search_height)
        self.txt_third_orderId.setFixedWidth(200)
        self.search_layout.addWidget(self.txt_third_orderId, 0, 1, 1, 1)
        # 导入时间 开始时间
        lb_import_date_start = QLabel()
        lb_import_date_start.setText("导入时间：")
        lb_import_date_start.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_import_date_start, 0, 2, 1, 1)
        self.time_import_date_start.setFixedHeight(txt_search_height)
        self.time_import_date_start.setDisplayFormat("yyyy-MM-dd")
        self.time_import_date_start.setCalendarPopup(True)
        self.time_import_date_start.setObjectName("import_date_start")
        self.search_layout.addWidget(self.time_import_date_start, 0, 3, 1, 1)
        # 导入时间 结束时间
        lb_import_date_end = QLabel()
        lb_import_date_end.setText("到")
        lb_import_date_end.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_import_date_end, 0, 4, 1, 1)
        self.time_import_date_end.setFixedHeight(txt_search_height)
        self.time_import_date_end.setDisplayFormat("yyyy-MM-dd")
        self.time_import_date_end.setCalendarPopup(True)
        self.time_import_date_end.setObjectName("import_date_end")
        self.search_layout.addWidget(self.time_import_date_end, 0, 5, 1, 1)
        # 到账时间 开始时间
        lb_receive_date_start = QLabel()
        lb_receive_date_start.setText("到账时间：")
        lb_receive_date_start.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_receive_date_start, 0, 6, 1, 1)
        self.time_receive_date_start.setFixedHeight(txt_search_height)
        self.time_receive_date_start.setDisplayFormat("yyyy-MM-dd")
        self.time_receive_date_start.setCalendarPopup(True)
        self.time_receive_date_start.setObjectName("receive_date_start")
        self.search_layout.addWidget(self.time_receive_date_start, 0, 7, 1, 1)
        # 到账时间 结束时间
        lb_receive_date_end = QLabel()
        lb_receive_date_end.setText("到")
        lb_receive_date_end.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_receive_date_end, 0, 8, 1, 1)
        self.time_receive_date_end.setFixedHeight(txt_search_height)
        self.time_receive_date_end.setDisplayFormat("yyyy-MM-dd")
        self.time_receive_date_end.setCalendarPopup(True)
        self.time_receive_date_end.setObjectName("receive_date_end")
        self.search_layout.addWidget(self.time_receive_date_end, 0, 9, 1, 1)
        # 支付方式
        lb_pay_type = QLabel()
        lb_pay_type.setText("支付方式：")
        lb_pay_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_pay_type, 0, 10, 1, 1)
        self.combo_pay_type.setObjectName("pay_type")
        self.combo_pay_type.setFixedHeight(txt_search_height)
        self.combo_pay_type.setFixedWidth(100)
        self.combo_pay_type.addItem('请选择', 0)
        for key, value in page_type.items():
            self.combo_pay_type.addItem(value, key)
        self.search_layout.addWidget(self.combo_pay_type, 0, 11, 1, 1)
        # 账单类型 收付款
        lb_account_type = QLabel()
        lb_account_type.setText("账单类型：")
        lb_account_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_layout.addWidget(lb_account_type, 0, 12, 1, 1)
        self.combo_account_type.setObjectName("account_type")
        self.combo_account_type.setFixedHeight(txt_search_height)
        self.combo_account_type.setFixedWidth(60)
        self.combo_account_type.addItem('请选择', 0)
        self.combo_account_type.addItem('收款', 1)
        self.combo_account_type.addItem('退款', 2)
        self.search_layout.addWidget(self.combo_account_type, 0, 13, 1, 1)
        btn_search = QPushButton()
        btn_search.setFixedWidth(menu_height)
        btn_search.setFixedHeight(lb_search_height)
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.clicked.connect(lambda: self.search_param(search_signal))
        self.search_layout.addWidget(btn_search, 0, 14, 1, 4)

    # 三方店铺
    def search_param(self, search_signal):
        self.sql_where = ''
        self.sql_where_value.clear()
        third_orderId = self.findChild(QLineEdit, 'third_orderId').text()
        if third_orderId is not None and len(third_orderId) > 0:
            self.sql_where += ' thirdOrderId = %s '
            self.sql_where_value.append(third_orderId)
        import_date_start = self.findChild(QDateTimeEdit, 'import_date_start').date()
        if import_date_start is not None:
            import_start = import_date_start.toString("yyyy-MM-dd")
            self.sql_where += ' and createdAt >= %s '
            self.sql_where_value.append(import_start + " 00:00:00")
        import_date_end = self.findChild(QDateTimeEdit, 'import_date_end').date()
        if import_date_end is not None:
            import_end = import_date_end.toString("yyyy-MM-dd")
            self.sql_where += ' and createdAt <= %s '
            self.sql_where_value.append(import_end + " 23:59:59")
        receive_date_start = self.findChild(QDateTimeEdit, 'receive_date_start').date()
        if receive_date_start is not None:
            receive_start = receive_date_start.toString("yyyy-MM-dd")
            self.sql_where += ' and receivePayTime >= %s '
            self.sql_where_value.append(receive_start + " 00:00:00")
        receive_date_end = self.findChild(QDateTimeEdit, 'receive_date_end').date()
        if receive_date_end is not None:
            receive_end = receive_date_end.toString("yyyy-MM-dd")
            self.sql_where += ' and receivePayTime <= %s '
            self.sql_where_value.append(receive_end + " 23:59:59")
        pay_type = self.findChild(QComboBox, 'pay_type').currentData()
        if pay_type is not None and str(pay_type) != '0':
            self.sql_where += ' and payType = %s '
            self.sql_where_value.append(str(pay_type))
        account_type = self.findChild(QComboBox, 'account_type').currentData()
        if account_type is not None and str(account_type) != '0':
            self.sql_where += ' and type = %s '
            self.sql_where_value.append(str(account_type))
        # 改变表格内容
        self.sql_where = self.sql_where.strip()
        if self.sql_where.startswith('and'):
            self.sql_where = self.sql_where[3:]
        self.sql_where = ' where ' + self.sql_where
        self.search_sql = {'sql_where': self.sql_where, 'sql_where_value': tuple(self.sql_where_value)}
        search_signal.emit({'search_param': self.search_sql, 'pageIndex': 1, 'pageSize': PAGE_SIZE})
