import sys
import os
import re
from src.Covert_UI import Ui_MainWindow
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QFileDialog
import logging
import xlrd
from src.xml_to_excel import XmlToExcel

# 定义所需数据所在的列
CASE_COL = 2
EXPECTED_RESULT_COL = CASE_COL+1  # 期望结果
PRIORITY_COL = CASE_COL + 5       # 优先级
COMMENT_COL = CASE_COL + 7        # 注释说明
CASE_NUM = 50                     # xml文件里最大用例个数
# 生成用例的xml模板
TESTCASE_TMPLATE = '''
                            <testcase name="{testcaseName}">
                                <summary><![CDATA[<p>{describeContent}</p>]]></summary>
                                <preconditions><![CDATA[<p>{testcaseComment}</p>]]>
                                </preconditions>
                                <execution_type><![CDATA[1]]></execution_type>
                                <importance><![CDATA[{iPriority}]]></importance>
                                <estimated_exec_duration></estimated_exec_duration>
                                <status>1</status>
                            <steps>
                            <step>
                                <step_number><![CDATA[1]]></step_number>
                                <actions><![CDATA[<p>{testcaseStep}</p>]]>
                                </actions>
                                <expectedresults><![CDATA[<p>{testcaseExpeRes}</p>]]>
                                </expectedresults>
                                <execution_type><![CDATA[1]]></execution_type>
                            </step>
                            </steps>
                            </testcase>
                            '''
# 测试组件的头模板
TESTSUITE_TMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
                <testsuite name="{testcaseSuiteName}" >
                <details><![CDATA[<p>{detail}测试</p>]]>
                </details> 
                <custom_fields>
                    <custom_field>
                        <name><![CDATA[]]></name>
                        <value><![CDATA[]]></value>
                    </custom_field>
                </custom_fields>
                '''
# 添加log记录错误消息
logger = logging.getLogger("error_log")
logger.setLevel(logging.ERROR)
# 日志写入文件的方式默认是追加写入，改为覆盖写入，即日志中记录当次运行出错信息
file_hander = logging.FileHandler("error_output.log", encoding="utf-8", mode="w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_hander.setFormatter(formatter)
logger.addHandler(file_hander)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置为只读，不允许用户自行输入路径，只能从浏览按钮选择路径
        self.excel_path_edit.setReadOnly(True)
        # 导出路径默认为程序所在路径
        self.current_path = os.path.dirname(__file__)
        self.xml_path_edit.setText(self.current_path)
        self.xml_path_edit.setReadOnly(True)
        self.exit.clicked.connect(self.exit_app)                    # 连接退出槽函数
        self.start_convert.clicked.connect(self.start_convert_run)  # 连接开始转换的槽函数
        self.excel_path_button.clicked.connect(self.select_excel_file)
        self.xml_path_button.clicked.connect(self.select_xml_file)
        self.excel_path = None
        self.xml_path = None

    # 开始转换
    def start_convert_run(self):
        try:
            # 检查并得到文件路径
            self.get_input_path()
            # 检查是否有返回值，无返回值代表输入的路径为空
            if self.excel_path and self.xml_path:
                self.convert()
        except Exception:
            logger.exception("运行出现异常，请查看日志", exc_info=True)

    # 转换
    def convert(self):
        # excel to xml
        if self.excel_to_xml.isChecked():
            self.convert_excel_to_xml()
        # xml to excel
        elif self.xml_to_excel.isChecked():
            self.convert_xml_to_exccel()

    def write_xml_to_file(self, sheet):
        if sheet and sheet.name != "Safeview" and sheet.name != "Issue List":    # 名为Safeview和Issue List的表格不需要转换，不是测试用例
            try:
                # 创建与输入的excel文件同名的文件夹，用于存放生成的xml文件(生成的xml文件可能有多个)
                xml_dir = os.path.join(self.xml_path, os.path.basename(self.excel_path).replace(".xlsx", ""))
                if not os.path.exists(xml_dir):
                    os.mkdir(xml_dir)
                self.write_xml_file_by_cnt(xml_dir, CASE_NUM, sheet)
                QMessageBox.information(self, "转换成功提示", "成功！xml文件保存在{path}路径下".format(path=os.path.abspath(xml_dir)))   # 写入完成后进行提示说明
            except Exception:
                logger.exception("转换失败", exc_info=True)

    # 往文件里写入cnt个用例
    def write_xml_file_by_cnt(self, xml_dir, cnt, sheet):
        '''
        :param xml_dir: the dir path to save the generation xml file
        :param cnt:  total count of test case in each xml file
        :param sheet: sheet in excel
        :return: None
        '''
        # 检测传入的参数，不正确是抛出异常
        if not xml_dir or cnt <= 0 or not sheet:
            raise Exception("write_xml_file_by_cnt函数中传入的参数不正确")

        index = 1   # 用来记录生成的xml文件编号（用于当excel中用例条数过多，生成的文件需要拆分成几个xml文件，eg:**1.xml,**2.xml ）
        text = self.generate_xml(sheet)  # 得到生成用例的生成器
        xml_file = os.path.basename(self.excel_path).replace(".xlsx",'')
        try:
            while text and True:
                f = open(os.path.join(xml_dir, xml_file+str(index)+'.xml'), "wb")   # sheet的名字作为生成的xml文件名，以字节的方式写入，就不会存在编码问题
                index += 1  # 编号递增
                count = cnt
                f.write(bytes(TESTSUITE_TMPLATE.format(testcaseSuiteName=str(sheet.name), detail=str(sheet.name)), encoding="utf-8"))  # 写进测试组
                while count:
                    f.write(bytes(next(text), encoding="utf-8"))
                    count -= 1
                f.write(bytes("</testsuite>", encoding="utf-8"))
                f.close()
        except StopIteration:
            # 跳出循环的时候，最后一段的用例数不够count条，在文件中继续写入套件结尾，并关闭文件
            if count!=cnt:
                f.write(bytes("</testsuite>", encoding="utf-8"))
                f.close()
            # 用例总数/n为整数，刚好能转换成用例总数/n个xml文件，移出新建的多余的文件
            else:
                # 先关闭文件再删除
                if not f.closed:
                    f.close()
                os.remove(os.path.abspath(os.path.join(xml_dir, sheet.name+str(index-1))))

    # 根据传入的表格生成相应的xml内容
    def generate_xml(self, sheet):
        '''
        :param sheet: the sheet in excel
        :return: a generator that generates every test case xml format content
        '''
        # 检测参数
        if not sheet and not sheet.name:
            raise Exception("generate_xml函数传入的sheet参数为空或者None")
        sheet_name = sheet.name
        if sheet_name and sheet_name != "Safeview" and sheet_name != "Issue List":
            # 获取表格行数和列数
            nrows = sheet.nrows
            # 找到开始的行数
            for row in range(nrows):
                if "Test Case Table" in sheet.row_values(row):
                    break
            row = row + 3           # 得到用例开始的行
            while row < nrows:
                # 得到测试用例相应的元素：标题、测试步骤、优先级、说明、期望结果
                testCaseContent = sheet.cell_value(row, CASE_COL)
                testcaseExpeRes = sheet.cell_value(row, EXPECTED_RESULT_COL)
                testcasePriority = sheet.cell_value(row, PRIORITY_COL)
                testcaseComment = sheet.cell_value(row, COMMENT_COL)
                testCaseName = ''
                tesetCaseSteps = []
                # 开始处理每一个元素
                testCaseItem = testCaseContent.split('测试步骤')
                if len(testCaseItem) == 2:
                    testCaseName = testCaseItem[0].replace("\n", "")
                    tesetCaseSteps = re.findall("^\d+.*\D$", testCaseItem[1], re.MULTILINE)  # 找到每一条测试步骤，存放在数组中

                # 没有写测试用例标题或测试步骤时
                elif len(testCaseItem) == 1:
                    tesetCaseSteps = re.findall("^\d+.*\D$", testCaseItem[0], re.MULTILINE)
                    # 测试步骤为空的情况
                    if not tesetCaseSteps:
                        testCaseName = testCaseItem[0]

                # 得到最终的测试步骤内容
                case_steps = r''
                for step in tesetCaseSteps:
                    tmp = '<p>'+step+'</p>'
                    case_steps += tmp

                # 得到最终的优先级级别
                if testcasePriority == 'H':
                    priority_num = 3
                else:
                    priority_num = 2
                row += 1
                # 返回每次生成的测试用例xml内容
                yield TESTCASE_TMPLATE.format(testcaseName=str(testCaseName), describeContent=str(testCaseName), testcaseComment=str(testcaseComment), iPriority=str(priority_num), testcaseStep=str(case_steps), testcaseExpeRes=str(testcaseExpeRes))

    # excel转换成xml
    def convert_excel_to_xml(self):
        try:

            workbook = xlrd.open_workbook(self.excel_path)  # 获取工作簿
            for sheet in workbook.sheets():
                self.write_xml_to_file(sheet)
        except Exception:
            logger.exception("excel转换xml过程出现异常", exc_info=True)
            QMessageBox.information(self, "转换失败提示", "详情请查看日志")

    # xml转换成excel
    def convert_xml_to_exccel(self):
        try:
            convert_instance = XmlToExcel(self.xml_path)
            content = convert_instance.generate_excel(self.xml_path)
            convert_instance.write_to_excel(self.excel_path, content, os.path.basename(str(self.xml_path)).replace(".xml", ''))
            QMessageBox.information(self, "转换成功提示", "生成的excel文件保存在{path}路径下".format(path= self.excel_path))
        except Exception:
            logger.exception("xml转换成excel过程中出现异常", exc_info=True)
            QMessageBox.information(self, "转换失败提示", "转换失败！详情请查看日志")

    # 验证并得到输入的源文件路径，和导出xml文件路径
    def get_input_path(self):

        excel_path = self.excel_path_edit.text()  # 导入的excel或xml文件路径
        xml_path = self.xml_path_edit.text()      # 导出的文件夹路径

        if len(excel_path) == 0:
            QMessageBox.information(self, "warning", "请输入要转换的xlsx或者xml格式文件路径！")
        elif self.excel_to_xml.isChecked() and not excel_path.endswith(".xlsx"):
            # 清空原有的
            self.xml_path = None
            self.excel_path = None
            self.excel_path_edit.setText('')
            QMessageBox.information(self, "warning", "输入文件必须是xlsx格式的文件！")
        elif self.xml_to_excel.isChecked() and not excel_path.endswith(".xml"):
            # 清空原有的
            self.xml_path = None
            self.excel_path = None
            self.excel_path_edit.setText('')
            QMessageBox.information(self, "warning", "输入文件必须是xml格式的文件！")
        elif len(xml_path)==0:
            QMessageBox.information(self, "waring", "请选择导出文件的存储路径")
        elif self.excel_to_xml.isChecked() and excel_path.endswith(".xlsx"):
            self.excel_path= excel_path
            self.xml_path = xml_path
        elif self.xml_to_excel.isChecked() and excel_path.endswith(".xml"):
            self.excel_path = xml_path
            self.xml_path = excel_path
        else:
            QMessageBox.information(self, "waring", "请先选择转换方式!")

    # 打开文件选择框，选择文件路径
    def select_excel_file(self):
        fname = QFileDialog.getOpenFileName(self, "选择文件", "/C")
        try:
            if fname[0]:
                self.excel_path_edit.setText(fname[0])
        except Exception:
            logger.exception("选择源文件出现异常", exc_info=True)
            self.close()

    # 打开文件夹选择框，选择保存路径
    def select_xml_file(self):
        dname = QFileDialog.getExistingDirectory(self, "Save Directory", "/C")  # 开始设置的文件夹路径
        try:
            if dname:
                self.xml_path_edit.setText(dname)   # 设置输入框显示选择的路径
            else:
                QMessageBox.information(self, "warning", "请选择转换完的文件存储路径")
        except Exception:
            logger.exception("选择存储路径出现异常", exc_info=True)
            self.close()

    # 退出程序
    def exit_app(self):
        self.close()

# 运行
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        exe = MainWindow()
        exe.show()
        sys.exit(app.exec_())
    except Exception:
        logger.exception("程序出现异常", exc_info=True)
