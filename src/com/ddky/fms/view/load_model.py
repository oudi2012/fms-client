# encoding=utf-8
import sys
import logging

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from src.com.ddky.fms.view.model.right_widget import RightWidget

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# sql 标题高度
lb_sql_height = 25


# 启动页面
class LoadWidget(QWidget):
    def __init__(self):
        super(LoadWidget, self).__init__()
        self.btn_main = QPushButton('load_01')
        self.btn_conn = QPushButton('load_02')
        self.btn_run = QPushButton('load_03')
        # 整个下半部分的布局
        self.layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.btn_run.setFixedWidth(80)
        self.btn_run.setFixedHeight(lb_sql_height)
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.clicked.connect(self.run_mysql)
        btn_layout.addWidget(self.btn_run)
        self.btn_conn.setFixedWidth(80)
        self.btn_conn.setFixedHeight(lb_sql_height)
        self.btn_conn.setCursor(Qt.PointingHandCursor)
        self.btn_conn.clicked.connect(self.run_mysql)
        btn_layout.addWidget(self.btn_conn)
        self.btn_main.setFixedWidth(80)
        self.btn_main.setFixedHeight(lb_sql_height)
        self.btn_main.setCursor(Qt.PointingHandCursor)
        self.btn_main.clicked.connect(self.run_mysql)
        btn_layout.addWidget(self.btn_main)
        self.layout.addLayout(btn_layout)
        self.cont_widget = RightWidget()
        self.layout.addWidget(self.cont_widget)
        self.setLayout(self.layout)

    # 测试数据库连接
    def run_mysql(self):
        print("sss")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = LoadWidget()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
