# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Covert_UI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        MainWindow.setMinimumSize(QtCore.QSize(400, 300))
        MainWindow.setMaximumSize(QtCore.QSize(400, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.excel_path_button = QtWidgets.QPushButton(self.centralwidget)
        self.excel_path_button.setObjectName("excel_path_button")
        self.gridLayout.addWidget(self.excel_path_button, 1, 3, 1, 1)
        self.xml_path_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.xml_path_edit.setObjectName("xml_path_edit")
        self.gridLayout.addWidget(self.xml_path_edit, 2, 1, 1, 2)
        self.xml_path_button = QtWidgets.QPushButton(self.centralwidget)
        self.xml_path_button.setObjectName("xml_path_button")
        self.gridLayout.addWidget(self.xml_path_button, 2, 3, 1, 1)
        self.excel_path_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.excel_path_edit.setObjectName("excel_path_edit")
        self.gridLayout.addWidget(self.excel_path_edit, 1, 1, 1, 2)
        self.xml_path_label = QtWidgets.QLabel(self.centralwidget)
        self.xml_path_label.setObjectName("xml_path_label")
        self.gridLayout.addWidget(self.xml_path_label, 2, 0, 1, 1)
        self.excel_path_label = QtWidgets.QLabel(self.centralwidget)
        self.excel_path_label.setObjectName("excel_path_label")
        self.gridLayout.addWidget(self.excel_path_label, 1, 0, 1, 1)
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setObjectName("exit")
        self.gridLayout.addWidget(self.exit, 3, 2, 1, 1)
        self.start_convert = QtWidgets.QPushButton(self.centralwidget)
        self.start_convert.setObjectName("start_convert")
        self.gridLayout.addWidget(self.start_convert, 3, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TestLink测试用例转换工具"))
        self.excel_path_button.setText(_translate("MainWindow", "浏览"))
        self.xml_path_button.setText(_translate("MainWindow", "浏览"))
        self.xml_path_label.setText(_translate("MainWindow", "导出XML文件路径"))
        self.excel_path_label.setText(_translate("MainWindow", "导入xlsx文件路径"))
        self.exit.setText(_translate("MainWindow", "退出"))
        self.start_convert.setText(_translate("MainWindow", "开始转换"))

