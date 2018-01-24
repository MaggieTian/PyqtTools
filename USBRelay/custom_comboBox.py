#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24
# @Author  : tianqi
# @File    : custom_comboBox.py
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal


class CustomComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def __init__(self, parent = None):
        super(CustomComboBox,self).__init__(parent)


    # 重写showPopup函数
    def showPopup(self):
        # self.popupAboutToBeShown.emit()
        self.clear()
        self.insertItem(0, "请选择继电器串口号")
        index = 1
        portlist = self.get_port_list()
        if portlist is not None:
            for i in portlist:
                self.insertItem(index, i)
                index += 1
        QComboBox.showPopup(self)

# 获取接入的所有串口号
    def get_port_list(self):
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            yield str(port)