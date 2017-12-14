#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11
# @Author  : tianqi
# @File    : util.py
from PyQt5.QtWidgets import QDesktopWidget, QProgressBar, QWidget
from process_window import ProcessWindow
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



    def start_analysis(self,log_path,result_path,find_data):

        try:
            log_file = open(log_path,"r")
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

            lines = log_file.readlines()
            for index, line in enumerate(lines):
                for k, v in result.items():
                    for text, info in v.items():
                        if line.find(text) > -1:
                            info['cnt'] += 1
                            info['line'].append(index)
            print(result)
            return True,result

        # 程序执行出现异常
        except Exception:
            return False


    def write_to_excel(self):
        pass

if __name__ == '__main__':
    log_path = r"C:\Users\qtian\Desktop\1212左右转向进全景.log"
    data = {'1': ['car_signals_handler/55, old: 0x0, new: 0x2', 'fb_layer_mgr_set_group_prio: set avm3d_ui prio to 101'], '2': ['car_live_info_mgr_set_signals/165, car signal 0x2', 'fb_layer_mgr_set_group_prio: set avm3d_ui prio to 101']}
    Util().start_analysis(log_path,"ss",data)








