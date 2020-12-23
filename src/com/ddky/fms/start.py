# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QTableWidget, QTableView, QHeaderView, QVBoxLayout, QApplication, QWidget, QLabel, \
    QHBoxLayout, QMainWindow, QFrame, QPushButton
from PyQt5.QtCore import Qt

from src.com.ddky.fms.entry.bill_entry import third_bill_map
from src.com.ddky.fms.jdbc.mysql_dml import querySQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


# 表格样式
def tableStyle():
    style_sheet = """
        QHeaderView#hHeader::section {
            background-color: #F5F5F5;
            border: none;
            height: 30;
            text-align: center;
            border-bottom: 1px solid #cccccc;
            border-right: 1px solid #cccccc;
        }
        QWidget#task_label {
            background-color: #ffffff;
            border: none;
            height: 30;
            text-align: center;
            border-bottom: 1px solid #cccccc;
            border-right: 1px solid #cccccc;
        }
    """
    return style_sheet


# 左侧样式
def leftStyle():
    style_sheet = """
        border: none;
        padding-left: 5px;
        border-left: 1px solid #95B8E7;
        border-right: 1px solid #95B8E7;
        background-image:url(images/left_menu_bg.png);
    """
    return style_sheet


# 分页样式
def pageStyle():
    style_sheet = """
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


# 主页面
class MainContainer(QWidget):
    def __init__(self):
        super(MainContainer, self).__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("财务客户端")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.center_layer = QHBoxLayout()
        self.top_menu()
        self.left_menu()
        self.setLayout(self.layout)
        sql_where = " order by id desc"
        select_sql = querySQLAndWhere("fms_third_bill", ",".join(third_bill_map.keys()), sql_where)
        sql_helper = MySQLHelper()
        result = sql_helper.queryByParam(select_sql, 40)
        self.right_data(third_bill_map, result)
        self.layout.addLayout(self.center_layer, 9)

    # 顶部控件
    def top_menu(self):
        top_frame = QWidget()
        top_frame.setAutoFillBackground(True)
        top_frame.palette = QPalette()
        top_frame.palette.setBrush(QPalette.Background, QBrush(QPixmap("images/top_banner_bg.png")))
        top_frame.setPalette(top_frame.palette)
        top_frame.setFixedHeight(64)
        self.layout.addWidget(top_frame, 1)

    # 左侧菜单
    def left_menu(self):
        left_frame = QWidget()
        left_frame.setStyleSheet("border: 1px solid gray; background-color: #FFFFFF;")
        title_label = QLabel(left_frame)
        title_label.setText("导航")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setStyleSheet(leftStyle())
        title_label.setFixedHeight(31)
        task_label = QLabel(left_frame)
        task_label.setText("任务列表")
        task_label.setAutoFillBackground(True)
        task_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        task_label.setStyleSheet(leftStyle())
        task_label.setFixedHeight(31)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(title_label)
        left_layout.addWidget(task_label)
        left_layout.setSpacing(0)
        left_layout.addStretch()
        left_frame.setLayout(left_layout)
        self.center_layer.addWidget(left_frame, 1)

    # 右侧内容
    def right_data(self, headers, dataList):
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
        model.setHorizontalHeaderLabels([title for title in headers.values()])
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
                model.setItem(r_index, c_index, item)
                c_index = c_index + 1
            r_index = r_index + 1
        tableView = QTableView()
        tableView.setModel(model)
        # 水平方向，表格大小扩展到适当的尺寸
        tableView.horizontalHeader().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        tableView.horizontalHeader().setObjectName("hHeader")
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableView.verticalHeader().setVisible(False)
        tableView.setStyleSheet(tableStyle())
        self.center_layer.addWidget(tableView, 9)

    # 设置分页
    def setPageController(self, page):
        """ 自定义页码控制器 """
        homePage = QPushButton("首页")
        prePage = QPushButton("< 上一页")
        nextPage = QPushButton("下一页")
        finalPage = QPushButton("尾页")
        self.totalPage.setText("共" + str(page) + "页")
        skip_label_pre = QLabel("跳到")
        skip_label_page = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self._home_page)
        prePage.clicked.connect(self._pre_page)
        nextPage.clicked.connect(self._next_page)
        finalPage.clicked.connect(self._final_page)
        confirmSkip.clicked.connect(self._confirm_skip)
        control_layout = QHBoxLayout()
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curtPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skip_label_pre)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skip_label_page)
        control_layout.addWidget(confirmSkip)
        self.layout.addLayout(control_layout)

    def _home_page(self):
        """ 点击首页信号 """
        self.control_signal.emit(["home", self.curtPage.text()])

    def _pre_page(self):
        """ 点击上一页信号 """
        self.control_signal.emit(["pre", self.curtPage.text()])

    def _next_page(self):
        """ 点击下一页信号 """
        self.control_signal.emit(["next", self.curtPage.text()])

    def _final_page(self):
        """ 末页点击信号 """
        self.control_signal.emit(["final", self.curtPage.text()])

    def _confirm_skip(self):
        """ 跳转页码确定 """
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """ 返回当前总页数 """
        return int(self.totalPage.text()[1:-1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = MainContainer()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
