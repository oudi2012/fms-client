# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFrame, QVBoxLayout, QLineEdit, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from src.com.ddky.fms.jdbc.mysql_dml import querySQLAndWhere, insertSQL
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# 搜索栏标题的高度
lb_search_height = 25
# 搜索栏输入框的高度
txt_search_height = 25
# 按钮高度
btn_search_height = 25


# 面包屑样式
def frameStyle():
    style_sheet = """
        #pathSetting {
            border: none;
            border-top: 1px solid #95B8E7;
        }
        QLabel {
            padding-left: 10px;
            border: none;
        }
    """
    return style_sheet


# 路径设置
class PathWidget(QFrame):

    def __init__(self):
        super(PathWidget, self).__init__()
        self.txt_ele = QLineEdit()
        self.txt_wm = QLineEdit()
        self.setObjectName("pathSetting")
        self.setStyleSheet(frameStyle())
        self.path_layout = QVBoxLayout()
        self.setLayout(self.path_layout)
        self.wmPath()
        self.elePath()
        self.path_layout.addStretch()
        self.getData()

    # 美团路径设置
    def wmPath(self):
        pathItem_layout = QHBoxLayout()
        lb_wm = QLabel()
        lb_wm.setObjectName("lb_wm")
        lb_wm.setFixedHeight(lb_search_height)
        lb_wm.setText("美团Excel文件路径：")
        pathItem_layout.addWidget(lb_wm)
        self.txt_wm.setObjectName("txt_wm")
        self.txt_wm.setFixedHeight(txt_search_height)
        self.txt_wm.setFixedWidth(300)
        pathItem_layout.addWidget(self.txt_wm)
        # 文件路径配置
        btn_browse_wm = QPushButton()
        btn_browse_wm.setText("浏览")
        btn_browse_wm.setObjectName("btn_browse_wm")
        btn_browse_wm.setAutoFillBackground(True)
        btn_browse_wm.setFixedHeight(btn_search_height)
        btn_browse_wm.setCursor(Qt.PointingHandCursor)
        btn_browse_wm.clicked.connect(self.wmOpenDialog)
        pathItem_layout.addWidget(btn_browse_wm)
        # 文件路径配置
        btn_save_wm = QPushButton()
        btn_save_wm.setText("保存")
        btn_save_wm.setObjectName("btn_save_wm")
        btn_save_wm.setAutoFillBackground(True)
        btn_save_wm.setFixedHeight(btn_search_height)
        btn_save_wm.setCursor(Qt.PointingHandCursor)
        btn_save_wm.clicked.connect(self.saveWmData)
        pathItem_layout.addWidget(btn_save_wm)
        # 添加扩展
        pathItem_layout.addStretch()
        self.path_layout.addLayout(pathItem_layout)

    # 饿百路径设置
    def elePath(self):
        pathItem_layout = QHBoxLayout()
        lb_ele = QLabel()
        lb_ele.setObjectName("lb_ele")
        lb_ele.setFixedHeight(lb_search_height)
        lb_ele.setText("饿百Excel文件路径：")
        pathItem_layout.addWidget(lb_ele)
        self.txt_ele.setObjectName("txt_ele")
        self.txt_ele.setFixedHeight(txt_search_height)
        self.txt_ele.setFixedWidth(300)
        pathItem_layout.addWidget(self.txt_ele)
        # 文件路径配置
        btn_browse_ele = QPushButton()
        btn_browse_ele.setText("浏览")
        btn_browse_ele.setObjectName("btn_browse_ele")
        btn_browse_ele.setAutoFillBackground(True)
        btn_browse_ele.setFixedHeight(btn_search_height)
        btn_browse_ele.setCursor(Qt.PointingHandCursor)
        btn_browse_ele.clicked.connect(self.eleOpenDialog)
        pathItem_layout.addWidget(btn_browse_ele)
        # 文件路径配置
        btn_save_ele = QPushButton()
        btn_save_ele.setText("保存")
        btn_save_ele.setObjectName("btn_save_ele")
        btn_save_ele.setAutoFillBackground(True)
        btn_save_ele.setFixedHeight(btn_search_height)
        btn_save_ele.setCursor(Qt.PointingHandCursor)
        btn_save_ele.clicked.connect(self.saveEleData)
        pathItem_layout.addWidget(btn_save_ele)
        # 添加扩展
        pathItem_layout.addStretch()
        self.path_layout.addLayout(pathItem_layout)

    # 打开文件管理器
    def wmOpenDialog(self):
        path = QFileDialog.getExistingDirectory(self, "文件路径选择", "C:\\Users\\Administrator\\Desktop")
        self.txt_wm.setText(path)

    # 打开文件管理器
    def eleOpenDialog(self):
        path = QFileDialog.getExistingDirectory(self, "文件路径选择", "C:\\Users\\Administrator\\Desktop")
        self.txt_ele.setText(path)

    # 保存数据
    def saveWmData(self):
        sql_helper = MySQLHelper()
        excel_param = {'name': 'wm', 'path': self.txt_wm.text(), 'createDate': 1}
        insert_sql = insertSQL('fms_excel_path', excel_param)
        wm_tuple = ('wm', self.txt_wm.text(), 1)
        sql_helper.insert(insert_sql, wm_tuple)
        sql_helper.dispose()

    # 保存数据
    def saveEleData(self):
        sql_helper = MySQLHelper()
        excel_param = {'name': 'ele', 'path': self.txt_ele.text(), 'createDate': 1}
        insert_sql = insertSQL('fms_excel_path', excel_param)
        wm_tuple = ('ele', self.txt_wm.text(), 1)
        sql_helper.insert(insert_sql, wm_tuple)
        sql_helper.dispose()

    # 获取数据
    def getData(self):
        sql_helper = MySQLHelper()
        select_sql = querySQLAndWhere('fms_excel_path', '*', '', '', None, None)
        dataList = sql_helper.queryByParam(select_sql)
        sql_helper.dispose()
        if dataList is not None:
            for dataItem in dataList:
                if dataItem['name'] == 'wm':
                    self.txt_wm.setText(dataItem['path'])
                elif dataItem['name'] == 'ele':
                    self.txt_ele.setText(dataItem['path'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = PathWidget()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
