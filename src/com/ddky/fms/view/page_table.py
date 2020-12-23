# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QPushButton,\
    QLabel, QLineEdit, QApplication
from PyQt5.QtCore import pyqtSignal


class PageTable(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(PageTable, self).__init__(*args, **kwargs)
        self.__init_ui()

    def __init_ui(self):
        self.curtPage = QLabel("1")
        self.totalPage = QLabel()
        self.skipPage = QLineEdit()
        style_sheet = """
            QTableWidget {
                border: none;
                background-color:rgb(240,240,240)
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
        # 3 行 5 列 的表格
        table = QTableWidget(3, 5)
        # 自适应宽度
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout = QVBoxLayout()
        self.layout.addWidget(table)
        self.setLayout(self.layout)
        # 添加样式
        self.setStyleSheet(style_sheet)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__init_ui()

    def __init_ui(self):
        self.resize(1200, 600)
        self.setWindowTitle("QTableWidget 加页码控制器")
        # 实例化表格
        self.table_widget = PageTable()
        # 表格设置页码控制
        self.table_widget.setPageController(10)
        self.table_widget.control_signal.connect(self.pageController)
        self.setCentralWidget(self.table_widget)

    def pageController(self, signal):
        total_page = self.table_widget.showTotalPage()
        if "home" == signal[0]:
            self.table_widget.curtPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                return
            self.table_widget.curtPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                return
            self.table_widget.curtPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.table_widget.curtPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                return
            self.table_widget.curtPage.setText(signal[1])
        # 改变表格内容
        self.changeTableContent()

    def changeTableContent(self):
        """ 根据当前页改变表格的内容 """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
