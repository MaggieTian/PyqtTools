# 主窗口，应用qt designer 生成的类
import sys
import time
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLCDNumber
from USBRelay_Ui import Ui_MainWindow
import serial
import serial.tools.list_ports

'''
设置日志信息记录
'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("usbrelay.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

'''
窗口中的事件信号连接等实现
'''


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.start.clicked.connect(self.start_run)  # 开始控制继电器
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)

        # 设置延时和循环次数的默认值
        self.lineEdit_wait.setText(str(6))
        self.lineEdit_loop.setText(str(10000))
        self.lineEdit_off_on.setText(str(6))
        self.serial = None

    def start_run(self):

        wait_time = self.lineEdit_wait.text()
        loop = self.lineEdit_loop.text()
        com = self.comboBox.currentText().split(" ")[0]
        logger.info("目前连接的串口号是{0}".format(com))
        off_to_on_time = self.lineEdit_off_on.text()
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
                self.lcdNumber.display(0)               # 每次运行之前初始化显示循环次数为0
                self.serial = serial.Serial(com, 9600)  # 打开串口
                self.thread = RunThread()
                # 设置串口、开关延时时间、循环重复次数
                self.thread.set_serial(self.serial)
                self.thread.set_loop(int(loop))
                self.thread.set_wait_time(int(wait_time))
                self.thread.set_off_to_on_time(int(off_to_on_time))
                # 发送信号显示
                self.thread.signal.connect(self.display)
                self.thread.done_signal.connect(self.compelted)
                self.thread.start()
                self.thread.quit()    # 运行结束后结束线程
            except Exception as e:
                QMessageBox.information(self, "Warning!", "发生错误!\n错误信息："+str(e))
                logger.error("转换输入值时发送错误\n"+str(e))


    # lcd组件接收到信号后显示数字
    def display(self, times):
        print(times)
        self.lcdNumber.display(times)

    def stop(self):
        try:
            # 按下停止键就结束线程，不进行下一步的循环
            self.thread.terminate()
            self.thread.wait(10)   # 确保线程终止
            logger.info("结束线程")
            if self.serial.isOpen(): # 检测串口是否关闭，若没关闭则关闭串口
                self.serial.close()
            self.start.setEnabled(True)
            self.stop_button.setEnabled(False)
        except Exception as e:
            logger.error("停止线程失败，错误信息：{0}".format(str(e)))

    def compelted(self, msg):
        logger.info("循环次数"+msg)
        QMessageBox.information(self,"提示","已完成{0}次上下电".format(msg.split(" ")[1]))
        self.start.setEnabled(True)
        self.stop_button.setEnabled(False)


class RunThread(QThread):
    signal = pyqtSignal(int)  # 定义信号
    done_signal =pyqtSignal(str)

    def __init__(self,parent = None):
        super().__init__()
        self._com_num = None         # 串口号
        self._loop = None            # 循环次数
        self._wait_time = None       # 等待时间
        self._off_to_on_time = None  # 继电器从进入下一次循环的等待时间
        self._serial = None          # 打开的串口对象

    def run(self):
        try:
            # 开始发送命令给继电器控制上下电
            for i in range(self._loop):
                self.signal.emit(i + 1)  # 发射信号
                self._serial.write(bytes.fromhex("A0 01 01 A2"))    # turn on
                time.sleep(self._wait_time)
                self._serial.write(bytes.fromhex("A0 01 00 A1"))    # turn off
                time.sleep(self._off_to_on_time)
            self._serial.close()                                    # close port
            self.done_signal.emit("Done {0}".format(str(self._loop)))   # 发出完成信号
        except Exception as e:
            logger.error("向继电器发送指令过程中出现了异常:{0}".format(e))
            raise e  # 抛出异常


    '''
    set方法，设置线程运行需要的参数：串口号、延时、循环数
    '''

    def set_serial(self,ser):
        self._serial = ser

    def set_loop(self,loop):
        self._loop = loop

    def set_wait_time(self, wait_time):
        self._wait_time = wait_time

    def set_off_to_on_time(self, seconds):
        self._off_to_on_time = seconds
# 调试
if __name__=='__main__':

    app = QApplication(sys.argv)
    exe = MainWindow()
    exe.show()
    sys.exit(app.exec_())
