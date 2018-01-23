# 主窗口，应用qt designer 生成的类
import sys

import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLCDNumber
from USBRelay_Ui import Ui_MainWindow
import serial
import serial.tools.list_ports


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.start.clicked.connect(self.start_run)  # 开始控制继电器
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        self.lineEdit_wait.setText(str(10))
        self.lineEdit_loop.setText(str(10000))

        # 读取目前设备上的所有串口，加入combox供用户选择
        portlist = self.get_port_list()
        index = 1
        for i in portlist:
            self.comboBox.insertItem(index, i)
            index +=1

    def start_run(self):
        wait_time = self.lineEdit_wait.text()
        loop = self.lineEdit_loop.text()
        com = self.comboBox.currentText()
        self.stop_button.setEnabled(True)

        # 判断是否选择了串口号
        if com == "请选择继电器串口号":
            QMessageBox.information(self, "Warning!", "请选择接入的继电器串口号！")

        # 判断输入的等待时间和循环次数是否为空，等待默认为10s，循环默认1000次
        elif (not wait_time) or (not loop):
            QMessageBox.information(self, "Warning!", "请输入开关等待时间")

        else:
            # 判断输入的等待时间和循环次数是否是正整数
            try:
                self.start.setEnabled(False)
                self.thread = RunThread()
                self.thread.set_com(com)
                self.thread.set_loop(int(loop))
                self.thread.set_wait_time(int(wait_time))
                self.thread.signal.connect(self.display)
                self.thread.done_signal.connect(self.compelted)
                self.thread.start()
            except ValueError:
                QMessageBox.information(self, "Warning!", "等待时间或者循环数只能是正整数，请检查输入")

    def get_port_list(self):
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            yield port[0]

    def display(self, times):
        print(times)
        self.lcdNumber.display(times)

    def stop(self):
        if self.thread:
            self.thread.terminate()
            print("停止线程")

    def compelted(self, msg):
        print(msg)
        QMessageBox.information(self,"提示","已完成{0}次上下电".format(msg.split(" ")[1]))
        self.start.setEnabled(True)




class RunThread(QThread):
    signal = pyqtSignal(int)  # 定义信号
    done_signal =pyqtSignal(str)

    def __init__(self,parent = None):
        super().__init__()
        self._com_num = None  # 串口号
        self._loop = None   # 循环次数
        self._wait_time = None # 等待时间

    def run(self):
        try:
            # 开始发送命令给继电器控制上下电
            ser = serial.Serial(self._com_num, 9600)  # open serial port
            for i in range(self._loop):
                ser.write(bytes.fromhex("A0 01 01 A2"))  # turn on
                time.sleep(self._wait_time)
                ser.write(bytes.fromhex("A0 01 00 A1")) # turn off
                time.sleep(6)
                self.signal.emit(i+1)  # 发射信号
            ser.close()  # close port
            self.done_signal.emit("Done {0}".format(str(self._loop)))   # 发出完成信号
        except Exception:
            pass

    def set_com(self,comnum):
        self._com_num = comnum

    def set_loop(self,loop):
        self._loop = loop

    def set_wait_time(self,wait_time):
        self._wait_time = wait_time

# 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = MainWindow()
    exe.show()
    sys.exit(app.exec_())
    # portlist = MainWindow.get_port_list()
    # for i in portlist:
    #     print(i)

    # ser = serial.Serial("COM20", 9600)
    # ser.write("\xA0\x01\x01\xA2".encode())  # turn on
