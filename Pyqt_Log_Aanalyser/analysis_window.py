#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11
# @Author  : tianqi
# @File    : analysis_window.py

import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QWidget, QFileDialog, QTextEdit, QMessageBox, QCheckBox, QProgressBar
from util import Util
from result_window import ResultWindow



class  AnalysisWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.cnt = 3                # 用来控制产生查找目标的数量
        self.ignore_case = False    # 控制查找是否忽略大小写
        self.find_txts = []          # 存放查找的多个目标
        self.log_path = ""           # 查找文件路径
        self.result_path = ""        # 存放查找结果路径
        self.elemen_dic = {}         # 存放查找信息输入框组件
        self.result_btn = {}         # 存放查看结果按钮组件
        self.data = {}               # 存放读取的查找输入框值
        self.util = Util()           # 调用UTIl类中的方法
        self.init_ui()
        self.result_window = None   # 弹出结果窗口
        self.result_data = None     # 用来存放查找分析结果

    # 初始化界面
    def init_ui(self):

        grid = QGridLayout()  # 设置表格布局
        grid.setSpacing(5)   # 设置组件间的间隔

        check_box = QCheckBox("忽略大小写", self)  #选择是否忽略大小写查找
        check_box.toggle()
        check_box.stateChanged.connect(self.is_ignore_case)
        grid.addWidget(check_box)

        # 每一行有查找目标的输入框和查看结果按钮
        for i in range(0,self.cnt):
            find_label = QLabel("查找目标")
            grid.addWidget(find_label,i+1,0)
            for j in range(0,2):
                find_txt= QLineEdit()
                self.elemen_dic[str(i+1)+'_'+str(j)] = find_txt  # 以"行_列"的方式存储组件
                grid.addWidget(find_txt,i+1,j+1)

            result_btn = QPushButton("查看结果")
            self.result_btn[str(i)] = result_btn    # 用一个字典存放所有的按钮，用于后续的控制
            result_btn.setEnabled(False)   # 查找分析结果还没出来时按钮是disable的
            result_btn.clicked.connect(partial(self.show_result,i+1))
            grid.addWidget(result_btn,i+1,j+2)




        start_btn = QPushButton("开始查找分析")
        start_btn.clicked.connect(self.analysis)
        add_btn =  QPushButton("添加查找目标")
        add_btn.clicked.connect(self.add_element)  # 添加查找目标和查看结果系列组件
        grid.addWidget(add_btn,i+2,j-1)
        grid.addWidget(start_btn,i+2,j+2)


        self.setLayout(grid)
        self.setGeometry(300,300,500,600)
        self.setWindowTitle("分析")
        self.util.center_pos(self)  # 设置窗口显示在屏幕中央

    # 添加查找目标和查看结果系列组件
    def add_element(self):
        self.cnt = self.cnt+1

    # 开始查找分析日志
    def analysis(self):
        self.data = {}  # 清空之前的信息

        # 读取每个输入框的值
        if self.elemen_dic:
            for k,v in self.elemen_dic.items():
                temp = k.split('_')
                if str(v.text()):
                    self.data.setdefault(temp[0],[]).append(str(v.text()))
            print(self.data)
            # 若未填写查找信息，则弹出提示框
            if not self.data:
                QMessageBox.information(self, "Warning!", "请输入查找至少一个目标")
            else:
                result,self.result_data = self.util.start_analysis(self.log_path,self.result_path,self.data)  # 开始进行查找分析
                if result:
                    QMessageBox.information(self,"提示","完成！请点击查看结果按钮查看结果")  # 提示查找分析完毕
                    for key,btn in self.result_btn.items():
                        btn.setEnabled(True)                           # 查找分析完毕后查看结果按钮enable

                else:
                    QMessageBox.information(self,"提示","失败，出现异常！")

    # 显示查找分析结果，打开相应的excel文件
    def show_result(self,n):

        self.result_window = ResultWindow()
        self.result_window.show()
        self.result_window.show_result(self.result_data,n)



    # 是否忽略大小写
    def is_ignore_case(self,state):
        if state == Qt.Checked:
            self.ignore_case = True









# 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = AnalysisWindow()
    exe.show()
    sys.exit(app.exec_())



