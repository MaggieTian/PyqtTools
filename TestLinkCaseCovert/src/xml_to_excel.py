import os,shutil
import xml.etree.ElementTree as ET
from openpyxl import load_workbook
# 定义所需数据所在的列
from openpyxl.styles import Alignment

ROW = 17
CASE_NUM = 2
CASE_COL = CASE_NUM+1             # Case开始的列
EXPECTED_RESULT_COL = CASE_COL+1  # 期望结果
PRIORITY_COL = CASE_COL + 5       # 优先级

'''
translate xml file to excel file 
'''

class XmlToExcel():
    def __init__(self):
        self.sheet = None

    def generate_excel(self, xml_path):
        '''

        :param xml_path: the path of xml file
        :return:  a generator that can generate excel case in every teset case
        '''

        # 开始解析xml文件
        tree = ET.ElementTree(file=xml_path)
        root = tree.getroot()                                       # 获取根节点
        # self.sheet = root.attrib['name']                            # 将表格名字更改为测试套的名字
        for child_root in root:
            if child_root.tag == "testcase":
                testcase_id = child_root.attrib['internalid']     # 写入testcase id
                testcase_title = child_root.attrib['name']          # 测试用例标题
                steps = ''                                          # 测试步骤
                expect_result = ''                                  # 期望结果
                priority = ''                                       # 优先级
                # 查找优先级
                for i in child_root.iterfind("importance"):
                    if int(i.text) == 3:
                        priority = 'H'

                # 利用xpath查找测试步骤和期望结果
                for i in child_root.iterfind("steps/step"):
                    for step in i.iterfind("actions"):
                        steps += step.text.replace(" ", '')
                    for result in i.iterfind("expectedresults"):
                        expect_result += result.text.replace("\n", '')
                # 利用段落标签分割出测试步骤
                step_item = steps.replace("</p>", "").split("<p>")
                step_content = ''
                for step in step_item:
                    if step:
                        step_content += step + '\n'
                steps = testcase_title+'\n' + step_content
                expect_result = expect_result.replace("<p>", "").replace("</p>", "").replace("\t", "").replace("\n","").replace(" ", '') + '\n'
                yield {"tesetcase_id": testcase_id, "tesetcase": steps, "expected_result": expect_result, "priority": priority}

    def write_to_excel(self,export_dir, content,name):
        '''

        :param export_dir: the directory that save the result excel file
        :param content:  the xml content after converting
        :param name: the result excel file name
        :return: None
        '''

        # 得到存放excel模板路径
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../template"))
        # 将模板中的内容复制到新建的excel文件中
        shutil.copyfile(os.path.join(template_dir, "template.xlsx"),os.path.join(export_dir, name + ".xlsx"))
        workbook = load_workbook(os.path.join(export_dir, name + ".xlsx"))          # 打开文件
        sheet = workbook.active                                                   # 获取正在显示的sheet
        row = ROW
        alignment = Alignment(horizontal='left', vertical='justify', text_rotation=2, wrap_text=True, shrink_to_fit=True, indent=0)
        # 将用例写进excel
        for line in content:
            # 写入ID
            cell = sheet.cell(row,CASE_NUM)
            cell.alignment = alignment
            cell.value = int(line['tesetcase_id'])
            # 写入测试标题和步骤
            cell = sheet.cell(row, CASE_COL)
            cell.value = line['tesetcase']
            # 写入期望结果
            cell = sheet.cell(row, EXPECTED_RESULT_COL)
            cell.value = line['expected_result']
            # 写入优先级
            cell = sheet.cell(row, PRIORITY_COL)
            cell.value = line['priority']
            row += 1
        workbook.save(os.path.join(export_dir, name + ".xlsx"))



if __name__ == "__main__":
    p =XmlToExcel()
    text = p.generate_excel(r"C:\Users\qtian\Desktop\autotest\PyqtTools\TestLinkCaseCovert\template\Read-only file system.xml")
    p.write_to_excel(r"C:\Users\qtian\Desktop\autotest\PyqtTools\TestLinkCaseCovert\template",text,"test_result")