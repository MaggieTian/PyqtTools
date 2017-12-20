#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11
# @Author  : tianqi
# @File    : util.py

from PyQt5.QtWidgets import QDesktopWidget, QProgressBar, QWidget, QMessageBox



class Util():

    def __init__(self):
        self.step = 0      # 用来记录实现查找分析函数时执行的步数，并反馈给进度条显示进度

    # 设置窗口在屏幕中央位置
    def center_pos(self,window):

        screen = QDesktopWidget().screenGeometry()  # 获取屏幕大小
        size = window.geometry()                    # 获取窗口大小
        window.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2) # 设置窗口位置在屏幕中央

    def show_process_dialog(self,window):

        process = QProgressBar(window)
        process.setWindowTitle("请稍等...")
        return  process



    def start_analysis(self,log_path,find_data):

        try:
            result_info = {}
            result = {}
            # 初始化存放每个查找信息的数据结构
            for k, v in find_data.items():
                for j in v:
                    data_unit = {'cnt': 0, 'line': []}
                    result_info[j] = data_unit
                result["查找目标_" + k] = result_info
                result_info = {}  # 清空当前循环存储的内容

            print(result)
            linenum = 0  # 记录文件行数

            '''with语句打开和关闭文件，包括抛出一个内部块异常。for line in f文件对象f视为一个迭代器，
             会自动的采用缓冲IO和内存管理，所以你不必担心大文件。'''

            with open(log_path,"rb") as f:     # 以二进制读取文件内容方式读取文件内容，转行成字符串进行操作，可解决编码问题
                for line in f:
                    linenum += 1
                    for k, v in result.items():
                        for text, info in v.items():
                            if str(line).find(text) > -1:
                                info['cnt'] += 1
                                info['line'].append(linenum)

                print (linenum)
                return True,result

        # 程序执行出现异常
        except Exception :
            raise  Exception
            # return False


    def write_to_excel(self):
        pass

if __name__ == '__main__':
    log_path = r"C:\Users\qtian\Desktop\1219.log"
    data = {'1': [' Kernel image', '333']}
    print (Util().start_analysis(log_path,data))








