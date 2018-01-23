# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'USBRelay_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.com_num = QtWidgets.QLabel(self.centralwidget)
        self.com_num.setGeometry(QtCore.QRect(150, 110, 61, 31))
        self.com_num.setObjectName("com_num")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(270, 110, 171, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.wait_time = QtWidgets.QLabel(self.centralwidget)
        self.wait_time.setGeometry(QtCore.QRect(140, 190, 71, 20))
        self.wait_time.setObjectName("wait_time")
        self.lineEdit_wait = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_wait.setGeometry(QtCore.QRect(270, 190, 171, 20))
        self.lineEdit_wait.setObjectName("lineEdit_wait")
        self.seconds = QtWidgets.QLabel(self.centralwidget)
        self.seconds.setGeometry(QtCore.QRect(450, 190, 41, 20))
        self.seconds.setObjectName("seconds")
        self.loop_times = QtWidgets.QLabel(self.centralwidget)
        self.loop_times.setGeometry(QtCore.QRect(150, 260, 54, 20))
        self.loop_times.setObjectName("loop_times")
        self.lineEdit_loop = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_loop.setGeometry(QtCore.QRect(270, 260, 171, 20))
        self.lineEdit_loop.setObjectName("lineEdit_loop")
        self.times = QtWidgets.QLabel(self.centralwidget)
        self.times.setGeometry(QtCore.QRect(450, 260, 31, 20))
        self.times.setObjectName("times")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(370, 440, 91, 41))
        self.start.setObjectName("start")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(180, 440, 91, 41))
        self.stop_button.setObjectName("stop_button")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(270, 350, 161, 41))
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.com_num.setText(_translate("MainWindow", "COM串口号"))
        self.comboBox.setItemText(0, _translate("MainWindow", "请选择继电器串口号"))
        self.wait_time.setText(_translate("MainWindow", "开关间隔时间"))
        self.seconds.setText(_translate("MainWindow", "秒（s）"))
        self.loop_times.setText(_translate("MainWindow", "循环次数"))
        self.times.setText(_translate("MainWindow", "次"))
        self.start.setText(_translate("MainWindow", "确定"))
        self.stop_button.setText(_translate("MainWindow", "停止"))

