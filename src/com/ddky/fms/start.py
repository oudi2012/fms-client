# encoding=utf-8
import sys
import os
import logging

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from win32com import client

from src.com.ddky.fms.jdbc.mysql_dml import totalSQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper
from src.com.ddky.fms.main_page import MainContainer
from src.com.ddky.fms.jdbc import mysql_config

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# sql 标题高度
lb_sql_height = 25
# sql 输入项高度
txt_sql_height = 25


# 面包屑样式
def sqlStyle():
    style_sheet = """
        QPushButton {
            border-radius:8px;
            border: 1px solid #95B8E7;
        }
        QPushButton:hover {
            border:2px solid #95B8E7;
        }
        QLineEdit {
            border: 1px solid #95B8E7;
        }
    """
    return style_sheet


# 启动页面
class StartWidget(QWidget):
    def __init__(self):
        super(StartWidget, self).__init__()
        self.btn_main = QPushButton('进入操作中心')
        self.btn_conn = QPushButton('连接测试')
        self.btn_run = QPushButton('启动数据库')
        self.lb_run_state = QLabel()
        self.animation = QPropertyAnimation(self, b'windowOpacity', self)
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.top_frame = QWidget()
        self.sql_frame = QWidget()
        self.sql_frame.resize(600, 400)
        self.sql_frame.setStyleSheet(sqlStyle())
        self.bottom_frame = QWidget()
        self.setWindowTitle("财务客户端数据库配置项")
        self.resize(800, 600)
        # 整个下半部分的布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.sql_widget()
        self.layout.addWidget(self.top_frame)
        self.layout.addWidget(self.sql_frame)
        self.layout.addWidget(self.bottom_frame)
        self.setLayout(self.layout)
        self.check_mysql()

    # 顶部控件
    def top_widget(self):
        lb_top = QLabel()
        lay_top = QHBoxLayout()
        lay_top.addWidget(lb_top)
        self.top_frame.setLayout(lay_top)

    # sql 配置项
    def sql_widget(self):
        sql_layout = QGridLayout()
        # 横向间距
        sql_layout.setHorizontalSpacing(0)
        # 纵向间距
        sql_layout.setVerticalSpacing(2)
        lb_left = QLabel()
        sql_layout.addWidget(lb_left, 0, 0, 1, 1)
        lb_address = QLabel()
        lb_address.setText("数据库连接地址：")
        lb_address.setFixedHeight(lb_sql_height)
        lb_address.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sql_layout.addWidget(lb_address, 0, 1, 1, 1)
        txt_sql_address = QLineEdit()
        txt_sql_address.setObjectName("sql_address")
        txt_sql_address.setFixedHeight(txt_sql_height)
        txt_sql_address.setFixedWidth(200)
        txt_sql_address.setText(mysql_config.DB_HOST)
        sql_layout.addWidget(txt_sql_address, 0, 2, 1, 1)
        lb_port = QLabel()
        lb_port.setText("数据库端口：")
        lb_port.setFixedHeight(lb_sql_height)
        lb_port.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sql_layout.addWidget(lb_port, 1, 1, 1, 1)
        txt_port = QLineEdit()
        txt_port.setObjectName("sql_port")
        txt_port.setFixedHeight(txt_sql_height)
        txt_port.setFixedWidth(200)
        txt_port.setText(str(mysql_config.DB_PORT))
        sql_layout.addWidget(txt_port, 1, 2, 1, 1)
        lb_user = QLabel()
        lb_user.setText("数据库用户名：")
        lb_user.setFixedHeight(lb_sql_height)
        lb_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sql_layout.addWidget(lb_user, 2, 1, 1, 1)
        txt_user = QLineEdit()
        txt_user.setObjectName("sql_user")
        txt_user.setFixedHeight(txt_sql_height)
        txt_user.setFixedWidth(200)
        txt_user.setText(mysql_config.DB_USER)
        sql_layout.addWidget(txt_user, 2, 2, 1, 1)
        lb_passwd = QLabel()
        lb_passwd.setText("数据库密码：")
        lb_passwd.setFixedHeight(lb_sql_height)
        lb_passwd.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sql_layout.addWidget(lb_passwd, 3, 1, 1, 1)
        txt_passwd = QLineEdit()
        txt_passwd.setObjectName("sql_passwd")
        txt_passwd.setFixedHeight(txt_sql_height)
        txt_passwd.setFixedWidth(200)
        txt_passwd.setText(mysql_config.DB_PASSWD)
        sql_layout.addWidget(txt_passwd, 3, 2, 1, 1)
        lb_running = QLabel()
        lb_running.setText("启动状态：")
        lb_running.setFixedHeight(lb_sql_height)
        lb_running.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sql_layout.addWidget(lb_running, 4, 1, 1, 1)
        self.lb_run_state.setText("未启动")
        self.lb_run_state.setFixedHeight(lb_sql_height)
        self.lb_run_state.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        sql_layout.addWidget(self.lb_run_state, 4, 2, 1, 1)
        btn_layout = QHBoxLayout()
        self.btn_run.setFixedWidth(80)
        self.btn_run.setFixedHeight(lb_sql_height)
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.setVisible(True)
        self.btn_run.clicked.connect(self.run_mysql)
        btn_layout.addWidget(self.btn_run)
        self.btn_conn.setFixedWidth(80)
        self.btn_conn.setFixedHeight(lb_sql_height)
        self.btn_conn.setCursor(Qt.PointingHandCursor)
        self.btn_conn.clicked.connect(self.check_conn)
        btn_layout.addWidget(self.btn_conn)
        btn_close = QPushButton('关闭')
        btn_close.setFixedWidth(80)
        btn_close.setFixedHeight(lb_sql_height)
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.close_frame)
        btn_layout.addWidget(btn_close)
        self.btn_main.setFixedWidth(80)
        self.btn_main.setFixedHeight(lb_sql_height)
        self.btn_main.setCursor(Qt.PointingHandCursor)
        self.btn_main.setVisible(False)
        self.btn_main.clicked.connect(self.to_main_frame)
        btn_layout.addWidget(self.btn_main)
        btn_frame = QWidget()
        btn_frame.setLayout(btn_layout)
        sql_layout.addWidget(btn_frame, 5, 1, 1, 3)
        self.sql_frame.setLayout(sql_layout)

    # 底部控件
    def bottom_widget(self):
        lb_bottom = QLabel()
        lay_bottom = QHBoxLayout()
        lay_bottom.addWidget(lb_bottom)
        self.bottom_frame.setLayout(lay_bottom)

    # 关闭窗口
    def close_frame(self):
        self.close()

    # 关闭当前页面，进入主页面
    def to_main_frame(self):
        self.close()
        # 显示窗口
        main_frame = MainContainer()
        main_frame.show()

    # 测试数据库连接
    def check_conn(self, sql_helper=None):
        sql_helper = MySQLHelper()
        count_sql = totalSQLAndWhere('fms_third_shopinfo', '')
        totalInfo = sql_helper.findOne(count_sql)
        if totalInfo is not None:
            self.btn_conn.setText("连接成功")
        else:
            self.btn_conn.setText("连接失败")

    # 检测 mysql 进程是否存在
    def check_mysql(self):
        wmi = client.GetObject('winmgmts:/root/cimv2')
        processes = wmi.ExecQuery('select * from Win32_Process')
        for process in processes:
            if process.Name.startswith('mysql'):
                self.lb_run_state.setText("已启动")
                self.btn_main.setVisible(True)
                self.btn_run.setVisible(False)

    # 启动mysql
    def run_mysql(self):
        pwd = os.getcwd()
        logging.info('服务当前路径：' + pwd)
        if 'src' in pwd:
            mysql_path = pwd[0:pwd.index('src') + 4]
            # 开发环境
            os.chdir(mysql_path + 'mariadb/bin')
        else:
            # 正式环境
            os.chdir(pwd + '/bin')
        os.system(r"start .\mysqld.exe --defaults-file=..\my.ini --port=%s" % mysql_config.DB_PORT)
        self.lb_run_state.setText("已启动")
        self.btn_run.setVisible(False)
        self.btn_main.setVisible(True)
        os.chdir(pwd)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = StartWidget()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
