#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : tianqi
# @File    : process_window.py
import sys
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
# from util import Util

class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.step = 0

        self.initUI()

    def initUI(self):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 50, 200, 25)
        # Util().center_pos(self)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('请稍等...')


# 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = ProcessWindow()
    exe.show()
    sys.exit(app.exec_())