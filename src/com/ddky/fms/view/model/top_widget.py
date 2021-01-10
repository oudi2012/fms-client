# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QApplication

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


# 左侧菜单
class TopWidget(QWidget):
    def __init__(self):
        super(TopWidget, self).__init__()
        self.palette = QPalette()
        self.setAutoFillBackground(True)
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("images/top_banner_bg.png")))
        self.setPalette(self.palette)
        self.setFixedHeight(64)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = TopWidget()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
