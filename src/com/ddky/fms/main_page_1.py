# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtSignal
from src.com.ddky.fms.view.model.left_menu import LeftMenu
from src.com.ddky.fms.view.model.right_widget import RightWidget
from src.com.ddky.fms.view.model.top_widget import TopWidget

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


class MainContainer(QWidget):
    # 分页信号
    menu_signal = pyqtSignal(dict)

    def __init__(self):
        super(MainContainer, self).__init__()
        self.animation = QPropertyAnimation(self, b'windowOpacity', self)
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("财务客户端")
        # 整个页面的布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 0, 2, 1)
        # 整个下半部分的布局
        self.center_layout = QHBoxLayout()
        self.top_widget = TopWidget()
        self.layout.addWidget(self.top_widget)
        self.menu_param = {'name': 'btn_task', 'title': '任务管理'}
        self.left_frame = LeftMenu(self.menu_param, self.menu_signal)
        self.center_layout.addWidget(self.left_frame, 1)
        self.right_widget = RightWidget(self.menu_param, self.menu_signal)
        self.center_layout.addWidget(self.right_widget, 9)
        self.layout.addLayout(self.center_layout)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = MainContainer()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
