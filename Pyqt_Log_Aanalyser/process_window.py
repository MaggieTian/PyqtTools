#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : tianqi
# @File    : process_window.py
import sys
from PyQt5.QtWidgets import QWidget,QApplication, QMainWindow, QTextEdit


# from util import Util

class ProcessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.step = 0

        self.initUI()

    def initUI(self):

        self.widget = QWidget()
        edit = QTextEdit(self.widget)
        self.setCentralWidget(self.widget)


# 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = ProcessWindow()
    exe.show()
    sys.exit(app.exec_())