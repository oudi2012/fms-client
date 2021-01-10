# -*- coding: utf-8 -*-

import logging

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


# 面包屑样式
def crumbStyle():
    style_sheet = """
        #crumb {
            border: none;
        }
        QLabel {
            padding-left: 5px;
            border: none;
        }
    """
    return style_sheet


# 面包屑
class CrumbWidget(QFrame):

    def __init__(self, menu_param):
        super(CrumbWidget, self).__init__()
        self.setFixedHeight(30)
        self.setStyleSheet(crumbStyle())
        self.setObjectName("crumb")
        lb_crumb = QLabel(self)
        lb_crumb.setObjectName("lb_crumb")
        lb_crumb.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lb_crumb.setText("控制台 -> " + menu_param['title'])
        crumb_layout = QHBoxLayout()
        crumb_layout.addWidget(lb_crumb)
        crumb_layout.setContentsMargins(0, 0, 5, 0)
        self.setLayout(crumb_layout)
