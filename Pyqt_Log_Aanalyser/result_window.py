#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : tianqi
# @File    : result_window.py
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QGridLayout, QLabel, QAction, QMessageBox,QFileDialog

from util import Util
import xlrd
import xlwt


class ResultWiget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    # 初始化界面
    def init_ui(self):

        self.grid = QGridLayout()  # 使用表格布局
        self.grid.setSpacing(10)  # 设置组件之间的间距
        find_txt = QLabel("查找目标",self)
        cnt = QLabel("计数",self)
        self.grid.addWidget(find_txt,1,0)
        self.grid.addWidget(cnt,1,6)
        self.setLayout(self.grid)

    # 显示查找结果

    def show_data(self,data,n):
        row = 2  # 结果显示起始行数
        for k, v in data.items():
            num = int(k.split('_')[1])
            if num == int(n):
                for text, line in v.items():
                    find_txt = QLabel(text, self)
                    cnt = QLabel(str(line['cnt']))
                    cnt.setStyleSheet("color: rgb(255, 6, 10)")
                    self.grid.addWidget(find_txt, row, 0)
                    self.grid.addWidget(cnt, row, 6)
                    row += 1






class ResultWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.util = Util()
        self.widget = None
        self.result_data = None
        self.seq = 0             # 记录是第几个查找目标
        self.init_ui()           # 初始化界面



    def init_ui(self):

        tool_bar= self.addToolBar("详细结果导出")
        write_action = QAction("详细结果导入excel",self)  # 添加工具栏将详细的查找分析结果导入excel文件
        write_action.triggered.connect(self.write_excel)

        tool_bar.addAction(write_action)
        self.widget = ResultWiget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle("查看结果")
        self.setGeometry(300,300,500,300)
        self.util.center_pos(self)

    # 显示查找结果
    def show_result(self,data,n):

        self.result_data = data
        self.seq = n
        self.widget.show_data(data,n)

    # 写入excel
    def write_excel(self):
        row = 0   # 控制行数
        col = 0   # 控制列数

        try:
            workbook = xlwt.Workbook("utf-8")
            worksheet = workbook.add_sheet("查找目标" + str(self.seq) + "result", cell_overwrite_ok=True)  # 创建表
            for k, v in self.result_data.items():
                if int(k.split("_")[1]) == self.seq:
                    for text, info in v.items():
                        worksheet.write(row, col, text)
                        worksheet.write(row, col + 1, info['cnt'])
                        for index, line in enumerate(info['line']):      # 写入行数
                            if line:
                                worksheet.write(index + 1, col, line)     # 查找信息可能会没有在log中出现，line为空
                        col += col + 2
            dname = QFileDialog.getSaveFileName(self, "Save Directory", "/C","Excel File(.xls)" )    # 开始设置的文件夹路径
            if dname[0]:
                workbook.save(dname[0]+".xls")
                QMessageBox.information(self.widget, "提示","导入完成！保存路径："+dname[0]+".xls")  # 提示文件保存路径
            else:
                QMessageBox.information(self.widget,"提示","请输入保存的文件名！")
        # 抛出异常
        except Exception:
            raise Exception





            # 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = ResultWindow()
    exe.show()
    data = {'查找目标_1': {'6666': {'cnt': 0, 'line': []}, '000': {'cnt': 0, 'line': []}}, '查找目标_2': {'33': {'cnt': 0, 'line': []}}}
    exe.show_result(data,1)
    sys.exit(app.exec_())


