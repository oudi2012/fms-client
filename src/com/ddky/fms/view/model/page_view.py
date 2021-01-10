# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout


# 分页样式
def pageStyle():
    style_sheet = """
        QPushButton {
            max-width: 20ex;
            max-height: 8ex;
            font-size: 12px;
        }
        QLineEdit {
            max-width: 30px;

        }
    """
    return style_sheet


# 表格数据显示和分页
class PageViewWidget(QWidget):
    # page_signal 分页信号
    page_signal = pyqtSignal(list)

    def __init__(self):
        super(PageViewWidget, self).__init__()
        self.totalPage = QLabel()
        self.skipPage = QLineEdit()
        self.curtPage = QLabel('1')
        self.page_signal.connect(self.pageController)
        self.setStyleSheet(pageStyle())
        self.setFixedHeight(40)
        self.page_widget()

    # 分页控件
    def page_widget(self):
        """ 自定义页码控制器 """
        self.skipPage.setObjectName("skipPage")
        pageSize = QLabel('每页显示0条')
        pageSize.setObjectName("pageSize")
        self.curtPage.setObjectName("curtPage")
        homePage = QPushButton("首页")
        prePage = QPushButton("< 上一页")
        nextPage = QPushButton("下一页 >")
        finalPage = QPushButton("尾页")
        self.totalPage.setObjectName("totalPage")
        self.totalPage.setText("共1页")
        skip_label_pre = QLabel("跳到")
        skip_label_page = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self._home_page)
        prePage.clicked.connect(self._pre_page)
        nextPage.clicked.connect(self._next_page)
        finalPage.clicked.connect(self._final_page)
        confirmSkip.clicked.connect(self._confirm_skip)
        page_layout = QHBoxLayout()
        page_layout.addWidget(pageSize)
        page_layout.addWidget(homePage)
        page_layout.addWidget(prePage)
        page_layout.addWidget(self.curtPage)
        page_layout.addWidget(nextPage)
        page_layout.addWidget(finalPage)
        page_layout.addWidget(self.totalPage)
        page_layout.addWidget(skip_label_pre)
        page_layout.addWidget(self.skipPage)
        page_layout.addWidget(skip_label_page)
        page_layout.addWidget(confirmSkip)
        page_layout.addStretch(1)
        self.setLayout(page_layout)

    def _home_page(self):
        """ 点击首页信号 """
        self.page_signal.emit(["home", self.curtPage.text()])

    def _pre_page(self):
        """ 点击上一页信号 """
        self.page_signal.emit(["pre", self.curtPage.text()])

    def _next_page(self):
        """ 点击下一页信号 """
        self.page_signal.emit(["next", self.curtPage.text()])

    def _final_page(self):
        """ 末页点击信号 """
        self.page_signal.emit(["final", self.curtPage.text()])

    def _confirm_skip(self):
        """ 跳转页码确定 """
        self.page_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """ 返回当前总页数 """
        return int(self.totalPage.text()[1:-1])

    # 分页跳转
    def pageController(self, signal):
        total_page = self.showTotalPage()
        if "home" == signal[0]:
            self.curtPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                return
            self.curtPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                return
            self.curtPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.curtPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                return
            self.curtPage.setText(signal[1])
