#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11
# @Author  : tianqi
# @File    : index_window.py


import sys
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QWidget, QFileDialog, QTextEdit, QMessageBox


from analysis_window import AnalysisWindow

from util import Util

class IndexWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.log_path=""                # 存放LOG文件路径
        self.result_path=""             # 存放分析结果路径
        self.analysy_window=None
        self.init_ui()                  # 初始化窗口UI

    def init_ui(self):

        file_label = QLabel("LOG文件")
        result_label = QLabel("分析结果")
        self.file_input = QLineEdit(self)      # 输入框，用于选择LOG存放路径
        self.result_input = QLineEdit(self)    # 输入框，用于选择存放分析结果路径

        # 选择文件路径按钮
        file_btn = QPushButton("打开",self)
        file_btn.setToolTip("选择要分析的LOG文件")      # 设置提示语
        file_btn.clicked.connect(self.show_filedialog)  # 点击打开按钮打开文件选择对话框

        result_btn = QPushButton("选择",self)
        result_btn.setToolTip("选择存放分析结果路径")
        result_btn.clicked.connect(self.show_directory)  # 点击打开按钮打开文件夹选择对话框

        next_btn =  QPushButton("下一步",self)
        next_btn.clicked.connect(self.next_step)

        grid = QGridLayout()              # 使用表格布局
        grid.setSpacing(10)               # 设置组件之间的间距

        # 设置个组件存放位置，在表格布局中所处行和列
        grid.addWidget(file_label, 1, 0)
        grid.addWidget(self.file_input, 1, 1)
        grid.addWidget(file_btn, 1, 2)

        grid.addWidget(result_label, 2, 0)
        grid.addWidget(self.result_input, 2, 1)
        grid.addWidget(result_btn, 2, 2)
        grid.addWidget(next_btn, 5, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350,300)
        self.setWindowTitle("Log Analyser")
        Util().center_pos(self)
        self.show()

    # 打开文件选择对话框，选择要分析的文件
    def show_filedialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open File', '/C')  # 默认打开C盘
        if fname[0]:

            self.file_input.setText(fname[0])   # 将选择的文件路径显示在文本框中
            self.log_path = fname[0]
        else:
            QMessageBox.information(self, "Warning!", "没有选择任何文件！")

    # 打开文件夹选择框，选择分析结果存放路径
    def show_directory(self):

        dname = QFileDialog.getExistingDirectory(self,"Save Directory","/C")  # 默认打开C盘
        if dname:
            self.result_path = dname
            self.result_input.setText(dname)
        else:
            QMessageBox.warning(self, "Warning!", "没有选择任何文件！")

    # 下一步进入分析设置页面
    def next_step(self):

        self.analysy_window = AnalysisWindow()
        self.analysy_window.show()                # 弹出分析设置窗口

        # 传递参数：文件路径和存放结果路径
        self.analysy_window.log_path = self.log_path
        self.analysy_window.result_path = self.result_path

if __name__ == '__main__':

    app = QApplication(sys.argv)
    exe = IndexWindow()
    sys.exit(app.exec_())














