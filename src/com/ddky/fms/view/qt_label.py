# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtCore import Qt


def linkHovered():
    print("当鼠标滑过 label2")


def linkClicked():
    print("当鼠标点击 label4")


class QLabelDemo(QWidget):
    def __init__(self):
        super(QLabelDemo, self).__init__()
        self.resize(500, 300)
        self.initUI()

    def initUI(self):
        # 第一个标签，显示文本
        label_01 = QLabel(self)
        # 设置背景图片
        label_01.setText("<font color = yellow> 这个是一个文本标签 </font>")
        # 建立画布，颜色为蓝色
        label_01.setAutoFillBackground(True)
        palette = QPalette()
        # 设置背景
        palette.setColor(QPalette.Window, Qt.blue)
        label_01.setPalette(palette)
        # 文本居中
        label_01.setAlignment(Qt.AlignCenter)

        # 第二个标签
        label_02 = QLabel(self)
        label_02.setText("<a href='#'>欢迎使用 Python GUI 程序</a>")
        label_02.linkHovered.connect(linkHovered)

        # 第三个标签 图片
        label_03 = QLabel(self)
        # 居中
        label_03.setAlignment(Qt.AlignCenter)
        label_03.setPixmap(QPixmap("../images/banner.jpg"))

        # 第四个标签，网站链接
        # 注意，触发事件和打开浏览器是互斥的
        label_04 = QLabel(self)
        # 网站导入， 首先要设置属性
        # 如何设置 True ,浏览器，如何为 False 槽函数
        label_04.setOpenExternalLinks(True)
        label_04.setText("<a href='http://www.baidu.com'>感谢关注</a>")
        # 居右
        label_04.setAlignment(Qt.AlignRight)
        # tip
        label_04.setToolTip("这是一个超链接")
        # 鼠标点击（和上面的打开网页是互斥的）
        label_04.linkActivated.connect(linkClicked)

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(label_01)
        vbox.addWidget(label_02)
        vbox.addWidget(label_03)
        vbox.addWidget(label_04)
        # 标题
        self.setWindowTitle("QLabel 控件演示")
        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = QLabelDemo()
    # 显示窗口
    label.show()
    # 建立循环
    sys.exit(app.exec_())
