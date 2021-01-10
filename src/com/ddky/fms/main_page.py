# -*- coding: utf-8 -*-

import sys
import logging

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QTableView, QHeaderView, QVBoxLayout, QApplication, QWidget, QLabel, \
    QHBoxLayout, QPushButton, QLineEdit, QGridLayout, QDateTimeEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime, QPropertyAnimation

from src.com.ddky.fms.entry.bill_entry import third_shop
from src.com.ddky.fms.entry.menu_table_param import param_menu_table
from src.com.ddky.fms.entry.pay_type_enum import page_type
from src.com.ddky.fms.entry.value_format import format_value
from src.com.ddky.fms.jdbc.mysql_dml import querySQLAndWhere, totalSQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper
from src.com.ddky.fms.view.model.left_menu import LeftMenu
from src.com.ddky.fms.view.model.top_widget import TopWidget

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# 默认单页显示数据条数
default_page_size = 30
# 菜单高度
menu_height = 25
# 搜索栏标题的高度
lb_search_height = 25
# 搜索栏输入框的高度
txt_search_height = 25


# 表格样式
def tableStyle():
    style_sheet = """
        QTableView {
            border: 1px solid #95B8E7;
        }
        QHeaderView#hHeader::section {
            background-color: #F5F5F5;
            border: none;
            height: 30;
            text-align: center;
            border-bottom: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
        }
        QWidget#task_label {
            background-color: #ffffff;
            border: none;
            height: 30;
            text-align: center;
            border-bottom: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
        }
        QTableView::item:hover {
            background-color: rgba(200,200,220,255);
        }
    """
    return style_sheet


# 左侧样式
def leftStyle():
    style_sheet = """
        QPushButton {
            border: none;
            text-align: center;
            border-left: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
            background-image:url(images/left_menu_bg.png);
        }
        #firstMenu {
            border: none;
            padding-left: 5px;
            border-left: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
            background-image:url(images/left_menu_first.png);
        }        
        QPushButton:hover {
            border:2px solid #95B8E7;
        }
    """
    return style_sheet


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


# 面包屑样式
def crumbStyle():
    style_sheet = """
        QWidget {
            border-left: 1px solid #95B8E7;
            border-top: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
        }
        QLabel {
            border: none;
        }
    """
    return style_sheet


# 搜索样式
def searchStyle():
    style_sheet = """
        QWidget {
            border-left: 1px solid #95B8E7;
            border-top: 1px solid #95B8E7;
            border-right: 1px solid #95B8E7;
        }
        QPushButton {
            border: none;
            border-radius:8px;
            background-image:url(images/btn_search.png);
        }
        QPushButton#sync_data {
            border: none;
            border-radius:8px;
            background-image:url(images/reload.png);
        }
        QPushButton#sync_data:hover {
            border:2px solid #95B8E7;
        }
        QPushButton:hover {
            border:2px solid #95B8E7;
        }
        QLineEdit {
            border: 1px solid #95B8E7;
        }
        QLabel {
            border: none;
            max-width: 80px;
        }
    """
    return style_sheet


# 分页计算
def page_info(pageIndex, pageSize, totalCount):
    if pageIndex is None or pageIndex <= 0:
        pageIndex = 1
    if pageSize is None or pageSize <= 0:
        pageSize = default_page_size
    if totalCount is None:
        totalCount = 0
    pages = totalCount / pageSize
    more = totalCount % pageSize
    if more > 0:
        pages = pages + 1
    if pages <= 0:
        pages = 1
    if pageIndex >= pages:
        pageIndex = pages
    start = (pageIndex - 1) * pageSize
    return {'pageIndex': int(pageIndex), 'pageSize': int(pageSize), 'totalCount': int(totalCount),
            'pages': int(pages), 'start': int(start)}


class MainContainer(QWidget):
    # 分页信号
    page_signal = pyqtSignal(list)
    # 当前选中的菜单名称
    crt_menu_name = 'btn_task'
    # 数据查询条件
    sql_where = ''
    # 条件对应的值
    sql_where_value = []

    def __init__(self):
        super(MainContainer, self).__init__()
        self.animation = QPropertyAnimation(self, b'windowOpacity', self)
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("财务客户端")
        self.tableView = QTableView()
        # 整个页面的布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 整个下半部分的布局
        self.center_layout = QHBoxLayout()
        # 整个右半部分的布局
        self.right_layer = QVBoxLayout()
        self.right_layer.setContentsMargins(0, 0, 0, 0)
        self.right_layer.setSpacing(0)
        top_widget = TopWidget()
        self.layout.addWidget(top_widget, 1)
        self.left_frame = LeftMenu()
        self.center_layout.addWidget(self.left_frame, 1)
        # 默认数据
        self.crumb_frame = QWidget()
        self.search_frame = QWidget()
        self.page_frame = QWidget()
        self.right_widget()
        self.setLayout(self.layout)
        self.data_list()

    # 数据文件路径配置
    def path_widget(self):
        path_frame = QWidget()
        path_layout = QVBoxLayout()
        path_frame.setLayout(path_layout)
        lb_crumb = self.crumb_frame.findChild(QLabel, "lb_crumb")
        lb_crumb.setText("控制台 -> 文件路径设置")
        pathItem_layout = QHBoxLayout()
        lb_wm = QLabel(path_frame)
        lb_wm.setObjectName("lb_wm")
        lb_wm.setText("美团Excel文件路径：")
        pathItem_layout.addWidget(lb_wm)
        txt_wm = QLineEdit()
        txt_wm.setObjectName("txt_wm")
        txt_wm.setFixedHeight(txt_search_height)
        txt_wm.setFixedWidth(200)
        pathItem_layout.addWidget(txt_wm)
        # 添加扩展
        pathItem_layout.addStretch()
        path_layout.addLayout(pathItem_layout)
        # 添加扩展
        path_layout.addStretch()
        self.right_layer.insertWidget(2, path_frame, 8)
        # 删除表格
        self.right_layer.itemAt(3).widget().setVisible(False)
        # 删除分页
        self.right_layer.itemAt(4).widget().setVisible(False)

    # 面包屑导航
    def crumb_widget(self):
        self.crumb_frame.setStyleSheet(crumbStyle())
        self.crumb_frame.setFixedHeight(30)
        crumb_layout = QHBoxLayout()
        self.crumb_frame.setLayout(crumb_layout)
        lb_crumb = QLabel(self.crumb_frame)
        lb_crumb.setObjectName("lb_crumb")
        lb_crumb.setText("控制台 -> 任务列表 ")
        crumb_layout.addWidget(lb_crumb)
        self.right_layer.addWidget(self.crumb_frame, 1)

    def default_search_widget(self, btn_name):
        # 恢复选中按钮的样式
        crt_btn = self.left_frame.findChild(QPushButton, self.crt_menu_name)
        if crt_btn is not None:
            crt_btn.setStyleSheet(leftStyle())
        self.crt_menu_name = btn_name
        # 删除 _search_frame
        _search_frame = self.findChild(QWidget, '_search_frame')
        if _search_frame is not None:
            _search_frame.deleteLater()
            self.search_frame = QWidget()
        if btn_name == 'btn_third_shop':
            self.thirdShop_search_widget()
        elif btn_name == 'btn_task':
            self.task_search_widget()
        elif btn_name == 'btn_third_bill':
            self.thirdBill_search_widget()
        # 设置选中按钮的样式
        # btn_name = self.left_frame.findChild(QPushButton, btn_name)
        # btn_name.setStyleSheet("border: none;")
        defaultParam = param_menu_table[self.crt_menu_name]
        # 设置当前选中项l
        self.crt_menu_name = str(defaultParam['btn_name'])
        lb_crumb = self.crumb_frame.findChild(QLabel, "lb_crumb")
        # 设置导航面包屑
        lb_crumb.setText("控制台 -> " + str(defaultParam['menu_name']))

    # 列表的搜索框
    def btn_search_widget(self, btn_name):
        self.default_search_widget(btn_name)
        self.data_list()

    # 任务列表的搜索框
    def task_search_widget(self):
        self.search_frame.setObjectName("_search_frame")
        self.search_frame.setFixedHeight(1)
        self.search_frame.setStyleSheet(searchStyle())
        task_search_layout = QGridLayout()
        self.search_frame.setLayout(task_search_layout)
        self.right_layer.insertWidget(1, self.search_frame, 1)

    def thirdBill_search_widget(self):
        self.search_frame.setObjectName("_search_frame")
        self.search_frame.setFixedHeight(50)
        self.search_frame.setStyleSheet(searchStyle())
        task_search_layout = QGridLayout()
        self.search_frame.setLayout(task_search_layout)
        # 横向间距
        task_search_layout.setHorizontalSpacing(5)
        # 纵向间距
        task_search_layout.setVerticalSpacing(0)
        lb_third_orderId = QLabel(self.search_frame)
        lb_third_orderId.setText("三方单号：")
        lb_third_orderId.setFixedHeight(lb_search_height)
        lb_third_orderId.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_third_orderId, 0, 0, 1, 1)
        txt_third_orderId = QLineEdit()
        txt_third_orderId.setObjectName("third_orderId")
        txt_third_orderId.setFixedHeight(txt_search_height)
        txt_third_orderId.setFixedWidth(200)
        task_search_layout.addWidget(txt_third_orderId, 0, 1, 1, 1)
        # 导入时间 开始时间
        lb_import_date_start = QLabel(self.search_frame)
        lb_import_date_start.setText("导入时间：")
        lb_import_date_start.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_import_date_start, 0, 2, 1, 1)
        time_import_date_start = QDateTimeEdit(QDateTime.currentDateTime())
        time_import_date_start.setFixedHeight(txt_search_height)
        time_import_date_start.setDisplayFormat("yyyy-MM-dd")
        time_import_date_start.setCalendarPopup(True)
        time_import_date_start.setObjectName("import_date_start")
        task_search_layout.addWidget(time_import_date_start, 0, 3, 1, 1)
        # 导入时间 结束时间
        lb_import_date_end = QLabel(self.search_frame)
        lb_import_date_end.setText("到")
        lb_import_date_end.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_import_date_end, 0, 4, 1, 1)
        time_import_date_end = QDateTimeEdit(QDateTime.currentDateTime())
        time_import_date_end.setFixedHeight(txt_search_height)
        time_import_date_end.setDisplayFormat("yyyy-MM-dd")
        time_import_date_end.setCalendarPopup(True)
        time_import_date_end.setObjectName("import_date_end")
        task_search_layout.addWidget(time_import_date_end, 0, 5, 1, 1)
        # 到账时间 开始时间
        lb_receive_date_start = QLabel(self.search_frame)
        lb_receive_date_start.setText("到账时间：")
        lb_receive_date_start.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_receive_date_start, 0, 6, 1, 1)
        time_receive_date_start = QDateTimeEdit(QDateTime.currentDateTime().addDays(3))
        time_receive_date_start.setFixedHeight(txt_search_height)
        time_receive_date_start.setDisplayFormat("yyyy-MM-dd")
        time_receive_date_start.setCalendarPopup(True)
        time_receive_date_start.setObjectName("receive_date_start")
        task_search_layout.addWidget(time_receive_date_start, 0, 7, 1, 1)
        # 到账时间 结束时间
        lb_receive_date_end = QLabel(self.search_frame)
        lb_receive_date_end.setText("到")
        lb_receive_date_end.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_receive_date_end, 0, 8, 1, 1)
        time_receive_date_end = QDateTimeEdit(QDateTime.currentDateTime().addDays(3))
        time_receive_date_end.setFixedHeight(txt_search_height)
        time_receive_date_end.setDisplayFormat("yyyy-MM-dd")
        time_receive_date_end.setCalendarPopup(True)
        time_receive_date_end.setObjectName("receive_date_end")
        task_search_layout.addWidget(time_receive_date_end, 0, 9, 1, 1)
        # 支付方式
        lb_pay_type = QLabel(self.search_frame)
        lb_pay_type.setText("支付方式：")
        lb_pay_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_pay_type, 0, 10, 1, 1)
        combo_pay_type = QComboBox()
        combo_pay_type.setObjectName("pay_type")
        combo_pay_type.setFixedHeight(txt_search_height)
        combo_pay_type.setFixedWidth(100)
        combo_pay_type.addItem('请选择', 0)
        for key, value in page_type.items():
            combo_pay_type.addItem(value, key)
        task_search_layout.addWidget(combo_pay_type, 0, 11, 1, 1)
        # 账单类型 收付款
        lb_account_type = QLabel(self.search_frame)
        lb_account_type.setText("账单类型：")
        lb_account_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_account_type, 0, 12, 1, 1)
        combo_account_type = QComboBox()
        combo_account_type.setObjectName("account_type")
        combo_account_type.setFixedHeight(txt_search_height)
        combo_account_type.setFixedWidth(60)
        combo_account_type.addItem('请选择', 0)
        combo_account_type.addItem('收款', 1)
        combo_account_type.addItem('退款', 2)
        task_search_layout.addWidget(combo_account_type, 0, 13, 1, 1)
        btn_search = QPushButton()
        btn_search.setFixedWidth(menu_height)
        btn_search.setFixedHeight(lb_search_height)
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.clicked.connect(self.thirdBill_search_param)
        task_search_layout.addWidget(btn_search, 0, 14, 1, 4)
        self.right_layer.insertWidget(1, self.search_frame, 1)

    # 三方店铺搜索
    def thirdShop_search_widget(self):
        self.search_frame.setObjectName("_search_frame")
        self.search_frame.setFixedHeight(50)
        self.search_frame.setStyleSheet(searchStyle())
        task_search_layout = QGridLayout()
        self.search_frame.setLayout(task_search_layout)
        # 横向间距
        task_search_layout.setHorizontalSpacing(5)
        # 纵向间距
        task_search_layout.setVerticalSpacing(0)
        lb_shop_name = QLabel(self.search_frame)
        lb_shop_name.setText("店铺名称：")
        lb_shop_name.setFixedHeight(lb_search_height)
        lb_shop_name.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_shop_name, 0, 0, 1, 1)
        txt_shop_name = QLineEdit()
        txt_shop_name.setObjectName("shop_name")
        txt_shop_name.setFixedHeight(txt_search_height)
        txt_shop_name.setFixedWidth(200)
        task_search_layout.addWidget(txt_shop_name, 0, 1, 1, 1)
        # 店铺编号
        lb_shop_id = QLabel(self.search_frame)
        lb_shop_id.setText("店铺编号：")
        lb_shop_id.setFixedHeight(lb_search_height)
        lb_shop_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        task_search_layout.addWidget(lb_shop_id, 0, 2, 1, 1)
        txt_shop_id = QLineEdit()
        txt_shop_id.setObjectName("shop_id")
        txt_shop_id.setFixedHeight(txt_search_height)
        txt_shop_id.setFixedWidth(200)
        task_search_layout.addWidget(txt_shop_id, 0, 3, 1, 1)
        btn_search = QPushButton()
        btn_search.setFixedWidth(menu_height)
        btn_search.setFixedHeight(lb_search_height)
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.clicked.connect(self.thirdShop_search_param)
        task_search_layout.addWidget(btn_search, 0, 4, 1, 1)
        sync_data = QPushButton()
        sync_data.setObjectName("sync_data")
        sync_data.setFixedWidth(menu_height)
        sync_data.setFixedHeight(lb_search_height)
        sync_data.setCursor(Qt.PointingHandCursor)
        sync_data.clicked.connect(self.thirdShop_search_param)
        task_search_layout.addWidget(sync_data, 0, 5, 1, 4)
        self.right_layer.insertWidget(1, self.search_frame, 1)

    # 右侧内容
    def right_widget(self):
        # 面包屑导航
        self.crumb_widget()
        # 任务列表搜索框
        self.default_search_widget(self.crt_menu_name)
        # 水平方向，表格大小扩展到适当的尺寸
        self.tableView.horizontalHeader().setResizeContentsPrecision(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setObjectName("hHeader")
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setStyleSheet(tableStyle())
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.right_layer.addWidget(self.tableView, 8)
        self.page_widget()
        self.center_layout.addLayout(self.right_layer, 9)
        self.layout.addLayout(self.center_layout, 9)
        self.page_signal.connect(self.pageController)

    # 分页控件
    def page_widget(self):
        """ 自定义页码控制器 """
        skipPage = QLineEdit()
        skipPage.setObjectName("skipPage")
        pageSize = QLabel('每页显示0条')
        pageSize.setObjectName("pageSize")
        curtPage = QLabel('1')
        curtPage.setObjectName("curtPage")
        homePage = QPushButton("首页")
        prePage = QPushButton("< 上一页")
        nextPage = QPushButton("下一页 >")
        finalPage = QPushButton("尾页")
        totalPage = QLabel()
        totalPage.setObjectName("totalPage")
        totalPage.setText("共1页")
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
        page_layout.addWidget(curtPage)
        page_layout.addWidget(nextPage)
        page_layout.addWidget(finalPage)
        page_layout.addWidget(totalPage)
        page_layout.addWidget(skip_label_pre)
        page_layout.addWidget(skipPage)
        page_layout.addWidget(skip_label_page)
        page_layout.addWidget(confirmSkip)
        page_layout.addStretch(1)
        self.page_frame.setLayout(page_layout)
        self.page_frame.setStyleSheet(pageStyle())
        self.page_frame.setFixedHeight(40)
        self.right_layer.addWidget(self.page_frame)

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
        model.setHorizontalHeaderLabels([title.split('|')[0] for title in headers.values()])
        r_index = 0
        for row in dataList:
            c_index = 0
            for key, value in headers.items():
                arr_val = value.split('|')
                if key not in row.keys() or row[key] is None:
                    item_value = ''
                else:
                    item_value = str(row[key])
                if len(item_value) > 0 and item_value[0] == 'b':
                    item_value = item_value[2:-1]
                item_value = format_value(arr_val[1], item_value)
                item = QStandardItem(item_value)
                model.setItem(r_index, c_index, item)
                c_index = c_index + 1
            r_index = r_index + 1
        self.tableView.setModel(model)

    def _home_page(self):
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        """ 点击首页信号 """
        self.page_signal.emit(["home", curtPage.text()])

    def _pre_page(self):
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        """ 点击上一页信号 """
        self.page_signal.emit(["pre", curtPage.text()])

    def _next_page(self):
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        """ 点击下一页信号 """
        self.page_signal.emit(["next", curtPage.text()])

    def _final_page(self):
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        """ 末页点击信号 """
        self.page_signal.emit(["final", curtPage.text()])

    def _confirm_skip(self):
        skipPage = self.page_frame.findChild(QLineEdit, "skipPage")
        """ 跳转页码确定 """
        self.page_signal.emit(["confirm", skipPage.text()])

    def showTotalPage(self):
        totalPage = self.page_frame.findChild(QLabel, "totalPage")
        """ 返回当前总页数 """
        return int(totalPage.text()[1:-1])

    # 分页跳转
    def pageController(self, signal):
        total_page = self.showTotalPage()
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        if "home" == signal[0]:
            curtPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                return
            curtPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                return
            curtPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            curtPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                return
            curtPage.setText(signal[1])
        # 改变表格内容
        self.data_list()

    # 三方店铺
    def thirdShop_search_param(self):
        self.sql_where = ''
        self.sql_where_value.clear()
        shop_name = self.findChild(QLineEdit, 'shop_name').text()
        if shop_name is not None and len(shop_name) > 0:
            self.sql_where += " (name like concat('%', %s, '%') or thirdName like concat('%', %s, '%') ) "
            self.sql_where_value.append(shop_name)
            self.sql_where_value.append(shop_name)
        shop_id = self.findChild(QLineEdit, 'shop_id').text()
        if shop_id is not None and len(shop_id) > 0:
            self.sql_where += " and (thirdShopId=%s or platformId=%s) "
            self.sql_where_value.append(shop_id)
            self.sql_where_value.append(shop_id)
        # 改变表格内容
        self.sql_where = self.sql_where.strip()
        if self.sql_where.startswith('and'):
            self.sql_where = self.sql_where[3:]
        self.sql_where = ' where ' + self.sql_where
        self.data_list()

    # 获取搜索参数值
    def thirdBill_search_param(self):
        self.sql_where = ''
        self.sql_where_value.clear()
        third_orderId = self.findChild(QLineEdit, 'third_orderId').text()
        if third_orderId is not None and len(third_orderId) > 0:
            self.sql_where += ' thirdOrderId = %s '
            self.sql_where_value.append(third_orderId)
        import_date_start = self.findChild(QDateTimeEdit, 'import_date_start').date()
        if import_date_start is not None:
            import_start = import_date_start.toString("yyyy-MM-dd")
            self.sql_where += ' and createdAt >= %s '
            self.sql_where_value.append(import_start + " 00:00:00")
        import_date_end = self.findChild(QDateTimeEdit, 'import_date_end').date()
        if import_date_end is not None:
            import_end = import_date_end.toString("yyyy-MM-dd")
            self.sql_where += ' and createdAt <= %s '
            self.sql_where_value.append(import_end + " 23:59:59")
        receive_date_start = self.findChild(QDateTimeEdit, 'receive_date_start').date()
        if receive_date_start is not None:
            receive_start = receive_date_start.toString("yyyy-MM-dd")
            self.sql_where += ' and receivePayTime >= %s '
            self.sql_where_value.append(receive_start + " 00:00:00")
        receive_date_end = self.findChild(QDateTimeEdit, 'receive_date_end').date()
        if receive_date_end is not None:
            receive_end = receive_date_end.toString("yyyy-MM-dd")
            self.sql_where += ' and receivePayTime <= %s '
            self.sql_where_value.append(receive_end + " 23:59:59")
        pay_type = self.findChild(QComboBox, 'pay_type').currentData()
        if pay_type is not None and str(pay_type) != '0':
            self.sql_where += ' and payType = %s '
            self.sql_where_value.append(str(pay_type))
        account_type = self.findChild(QComboBox, 'account_type').currentData()
        if account_type is not None and str(account_type) != '0':
            self.sql_where += ' and type = %s '
            self.sql_where_value.append(str(account_type))
        # 改变表格内容
        self.sql_where = self.sql_where.strip()
        if self.sql_where.startswith('and'):
            self.sql_where = self.sql_where[3:]
        self.sql_where = ' where ' + self.sql_where
        self.data_list()

    # 三方店铺数据
    def data_list(self):
        # 根据按钮名称获取默认参数
        sql_helper = MySQLHelper()
        defaultParam = param_menu_table[self.crt_menu_name]
        curtPage = self.page_frame.findChild(QLabel, "curtPage")
        pageIndex = int(curtPage.text())
        pageSize = int(defaultParam['page_size'])
        lb_pageSize = self.findChild(QLabel, 'pageSize')
        lb_pageSize.setText("每页显示" + str(pageSize) + "条")
        # 获取总量
        count_sql = totalSQLAndWhere(str(defaultParam['table_name']), '')
        totalInfo = sql_helper.findOne(count_sql)
        # 设置页码
        pageInfo = page_info(pageIndex, pageSize, int(totalInfo['total']))
        totalPage = self.findChild(QLabel, 'totalPage')
        totalPage.setText("共" + str(pageInfo['pages']) + "页")
        # 获取具体数据
        sql_order = " order by id desc"
        select_sql = querySQLAndWhere(str(defaultParam['table_name']),
                                      ",".join(defaultParam['entry_map'].keys()), self.sql_where,
                                      sql_order, pageInfo['start'], pageSize)
        if len(self.sql_where_value) > 0:
            result = sql_helper.queryByParam(select_sql, pageSize, self.sql_where_value)
        else:
            result = sql_helper.queryByParam(select_sql, pageSize)
        sql_helper.dispose()
        if len(result) <= 0:
            result.append(third_shop)
        self.right_data(defaultParam['entry_map'], result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = MainContainer()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
