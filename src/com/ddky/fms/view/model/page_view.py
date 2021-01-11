# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout


# 分页样式
from src.com.ddky.fms.entry.bill_config import PAGE_SIZE


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

    def __init__(self, page_signal):
        super(PageViewWidget, self).__init__()
        self.pageSize = QLabel('每页显示0条')
        self.totalPage = QLabel()
        self.skipPage = QLineEdit()
        self.curtPage = QLabel('1')
        self.setStyleSheet(pageStyle())
        self.setFixedHeight(40)
        self.page_widget(page_signal)

    # 分页控件
    def page_widget(self, page_signal):
        """ 自定义页码控制器 """
        self.skipPage.setObjectName("skipPage")
        self.pageSize.setObjectName("pageSize")
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
        homePage.clicked.connect(lambda: self._home_page(page_signal))
        prePage.clicked.connect(lambda: self._pre_page(page_signal))
        nextPage.clicked.connect(lambda: self._next_page(page_signal))
        finalPage.clicked.connect(lambda: self._final_page(page_signal))
        confirmSkip.clicked.connect(lambda: self._confirm_skip(page_signal))
        page_layout = QHBoxLayout()
        page_layout.addWidget(self.pageSize)
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

    def _home_page(self, page_signal):
        """ 点击首页信号 """
        self.curtPage.setText(str(1))
        page_signal.emit([1, PAGE_SIZE])

    def _pre_page(self, page_signal):
        """ 点击上一页信号 """
        crt = int(self.curtPage.text())
        if 1 == crt:
            return
        self.curtPage.setText(str(crt - 1))
        page_signal.emit([crt - 1, PAGE_SIZE])

    def _next_page(self, page_signal):
        """ 点击下一页信号 """
        total_page = self.showTotalPage()
        crt = int(self.curtPage.text())
        if total_page == crt:
            return
        self.curtPage.setText(str(crt + 1))
        page_signal.emit([crt + 1, PAGE_SIZE])

    def _final_page(self, page_signal):
        """ 末页点击信号 """
        total_page = self.showTotalPage()
        self.curtPage.setText(str(total_page))
        page_signal.emit([total_page, PAGE_SIZE])

    def _confirm_skip(self, page_signal):
        """ 跳转页码确定 """
        total_page = self.showTotalPage()
        skip = self.skipPage.text()
        if skip is None or skip == '' or len(skip) <= 0:
            return
        if total_page < int(skip) or int(skip) < 0:
            return
        self.curtPage.setText(skip)
        page_signal.emit([int(skip), PAGE_SIZE])

    def showTotalPage(self):
        """ 返回当前总页数 """
        return int(self.totalPage.text()[1:-1])
