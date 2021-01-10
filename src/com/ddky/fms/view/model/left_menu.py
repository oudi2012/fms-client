# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QTableView, QHeaderView, QVBoxLayout, QApplication, QWidget, QLabel, \
    QHBoxLayout, QPushButton, QLineEdit, QGridLayout, QDateTimeEdit, QComboBox, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime, QPropertyAnimation

from src.com.ddky.fms.entry.menu_table_param import param_menu_table
from src.com.ddky.fms.view.model.right_widget import RightWidget

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# 菜单高度
menu_height = 25


# 左侧样式
def leftStyle():
    style_sheet = """
        #leftwidget {
            border: none;
            border-left: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
            border-bottom: 1px solid #95B8E7;
        }
        QPushButton {
            border: none;
            text-align: center;
            border-bottom: 1px solid #95B8E7;
            background-image:url(images/left_menu_bg.png);
        }
        #firstMenu {
            border: none;
            padding-left: 5px;
            border-bottom: 1px solid #95B8E7;
            background-image:url(images/left_menu_first.png);
        }        
        QPushButton:hover {
            border:2px solid #95B8E7;
        }
    """
    return style_sheet


# 左侧菜单
class LeftMenu(QFrame):

    def __init__(self, menu_param, menu_signal):
        super(LeftMenu, self).__init__()
        self.menu_param = menu_param
        self.left_widget(menu_signal)
        self.setObjectName("leftwidget")
        self.setStyleSheet(leftStyle())

    # 左侧菜单
    def left_widget(self, menu_signal):
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        self.setStyleSheet("border: 1px solid #95B8E7; background-color: #FFFFFF;")
        # 导航菜单
        lb_title = QLabel(self)
        lb_title.setText("导航")
        lb_title.setObjectName("firstMenu")
        lb_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lb_title.setFixedHeight(menu_height + 1)
        left_layout.addWidget(lb_title)
        # 任务菜单
        btn_task = QPushButton(self)
        btn_task.setText("任务管理")
        btn_task.setObjectName('btn_task')
        btn_task.setStyleSheet("background-image:url(none)")
        btn_task.setAutoFillBackground(True)
        btn_task.setFixedHeight(menu_height)
        btn_task.clicked.connect(lambda: self.menu_target('btn_task', '任务管理', menu_signal))
        btn_task.setCursor(Qt.PointingHandCursor)
        left_layout.addWidget(btn_task)
        # 三方账单
        btn_third_bill = QPushButton(self)
        btn_third_bill.setText("三方账单")
        btn_third_bill.setObjectName('btn_third_bill')
        btn_third_bill.setAutoFillBackground(True)
        btn_third_bill.setFixedHeight(menu_height)
        btn_third_bill.setCursor(Qt.PointingHandCursor)
        btn_third_bill.clicked.connect(lambda: self.menu_target('btn_third_bill', '三方账单', menu_signal))
        left_layout.addWidget(btn_third_bill)
        # 三方店铺
        btn_third_shop = QPushButton(self)
        btn_third_shop.setText("三方店铺")
        btn_third_shop.setObjectName("btn_third_shop")
        btn_third_shop.setAutoFillBackground(True)
        btn_third_shop.setFixedHeight(menu_height)
        btn_third_shop.setCursor(Qt.PointingHandCursor)
        btn_third_shop.clicked.connect(lambda: self.menu_target('btn_third_shop', '三方店铺', menu_signal))
        left_layout.addWidget(btn_third_shop)
        # 文件路径配置
        btn_excel_path = QPushButton(self)
        btn_excel_path.setText("路径配置")
        btn_excel_path.setObjectName("btn_excel_path")
        btn_excel_path.setAutoFillBackground(True)
        btn_excel_path.setFixedHeight(menu_height)
        btn_excel_path.setCursor(Qt.PointingHandCursor)
        btn_excel_path.clicked.connect(lambda: self.menu_target('btn_excel_path', '路径配置', menu_signal))
        left_layout.addWidget(btn_excel_path)
        # 添加扩展
        left_layout.addStretch()
        self.setLayout(left_layout)

    def menu_target(self, btn_name, btn_title, menu_signal):
        # 恢复选中按钮的样式
        crt_btn = self.findChild(QPushButton, self.menu_param['name'])
        if crt_btn is not None:
            crt_btn.setStyleSheet(leftStyle())
        self.menu_param = {'name': btn_name, 'title': btn_title}
        # 删除 _search_frame
        # 设置选中按钮的样式
        btn_widget = self.findChild(QPushButton, btn_name)
        btn_widget.setStyleSheet("background-image: url(none);")
        # 设置当前选中项
        menu_signal.emit(self.menu_param)
