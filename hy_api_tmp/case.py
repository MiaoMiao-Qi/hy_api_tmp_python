# coding: utf-8
# Purpose：接口自动化测试
# Author：Joyce
# 参考Blog：http://www.bstester.com/2015/08/interface-test-automation-scheme-details

import json
import re
import os
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import requests
import random
import const
import time
import setting as info
from LogUtils.logutil import LoggerUtil
logger = LoggerUtil()


case_list = []
ok = 0
ng = 0
num = 0
null = 0


class Excel:
    ROW_G = 1
    
    def __init__(self, path, new_path):
        if not os.path.exists(path):
            print('测试用例文件不存在！！！')
            sys.exit()
        self.api_file = xlrd.open_workbook(path, formatting_info=True)
        self.api_sheet = self.api_file.sheet_by_index(0)

        self.cases = []
        self.data_copy = copy(self.api_file)
        self.sheet = self.data_copy.get_sheet(0)
        self.new_path = new_path
        
    def get_cases(self):
        # 读取excel中每一行的值
        for line in range(1, self.api_sheet.nrows):
            case = Case()
            case.line = line
            case.num = int(self.api_sheet.cell(line, 0).value)
            case.module = self.api_sheet.cell(line, 1).value
            case.purpose = self.api_sheet.cell(line, 2).value
            case.host = self.api_sheet.cell(line, 3).value.replace('\n', '').replace('\r', '')
            case.url = self.api_sheet.cell(line, 4).value.replace('\n', '').replace('\r', '')
            case.params = self.api_sheet.cell(line, 5).value.replace('\n', '').replace('\r', '')
            case.method = self.api_sheet.cell(line, 6).value.replace('\n', '').replace('\r', '')
            case.checkpoint = self.api_sheet.cell(line, 7).value.replace('\n', '').replace('\r', '')
            case.variables = self.api_sheet.cell(line, 8).value.replace('\n', '').replace('\r', '')
            # 读的是入参可变参数列
            case.va_in_para = self.api_sheet.cell(line, 9).value.replace('\n', '').replace('\r', '')
            case.test_env = self.api_sheet.cell(line, 10).value.replace('\n', '').replace('\r', '')
            case.uat_env = self.api_sheet.cell(line, 11).value.replace('\n', '').replace('\r', '')
            case.active_online = self.api_sheet.cell(line, 12).value.replace('\n', '').replace('\r', '')
            self.cases.append(case)
            if case.va_in_para:
                Excel.ROW_G = line
        return self.cases

    def set_out_cell(self, row, col, value):
        """
        excel编辑写入
        :param row: 行
        :param col: 列
        :param value: 写入值
        :return:
        """
        out_sheet = self.sheet
        def _get_out_cell(out_sheet, row_index, col_index):
            row = out_sheet._Worksheet__rows.get(row_index)
        
            if not row:
                return None
        
            cell = row._Row__cells.get(col_index)
            return cell
    
        previous_cell = _get_out_cell(out_sheet, row, col)
    
        out_sheet.write(row, col, value)
        if previous_cell:
            new_cell = _get_out_cell(out_sheet, row, col)
            if new_cell:
                new_cell.xf_idx = previous_cell.xf_idx
    
    def save_excel(self):
        """
        保存excel文件
        :return:
        """
        try:
            self.data_copy.save(self.new_path)
        except:
            raise Exception("excel 文件正在被占用,请关闭后重试")
        
    def set_style(self, name, size, color, borders_size, color_fore, blod=False):
        """
        设置exeel风格
        :param name: 字体
        :param size: 大小
        :param color: 颜色
        :param borders_size: 边框
        :param color_fore:
        :param blod:
        :return:
        """
        style = xlwt.XFStyle()  # 初始化样式
        # 字体
        font = xlwt.Font()
        font.name = name
        font.height = 20 * size  # 字号
        font.bold = blod  # 加粗
        font.colour_index = color  # 默认：0x7FFF 黑色：0x08
        style.font = font
        # 居中
        alignment = xlwt.Alignment()  # 居中
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment

        alignment.wrap = 1
        # 边框
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = borders_size  # 自定义：1：细线；2：中细线；3：虚线；4：点线
        style.borders = borders
        # 背景颜色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置背景颜色的模式(NO_PATTERN; SOLID_PATTERN)
        pattern.pattern_fore_colour = color_fore  # 默认：无色：0x7FFF；黄色：0x0D；蓝色：0x0C
        style.pattern = pattern

        return style
    
    def color_execl(self, file_name):
        """
        给指定的单元格设置背景色
        :param file_name:文件路径
        :return:
        """
        style_bkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
        rb = xlrd.open_workbook(file_name, formatting_info=True)
        ro = rb.sheets()[0]
        wb = copy(rb)
        ws = wb.get_sheet(0)
        # 结果列
        col = 15
        for i in range(1, ro.nrows):
            result = ro.cell(i, col).value
            if result == "Fail":
                ws.write(i, col, ro.cell(i, col).value, style_bkg)
        wb.save(file_name)


class Case:
    VA_IN_PARAM = ''
    va_in_para = ''
    
    def __init__(self):
        self.line = 1
        self.num = 1
        self.module = ""
        self.purpose = ""
        self.host = ""
        self.url = ""
        self.params = ""
        self.method = "GET"
        self.checkpoint = '"status":1'
        self.variables = ""
        self.active = "No"
        self.active_online = "No"
        self.entire_url = ""
        self.result = ""
        self.response = ""
        self.proxies = {}
        self.elapsed = ""
        
        self.uat_env = "No"
        self.test_env = 'No'
        self.va_in_para = ""
        self.result_value = ""
        self.result_value_mail = ""
        self.code = ""
        
        # 失败时间段
        self.fail_time = ""
        # 响应时长
        self.response_time = ""
        # 实际入参
        self.actual_params = ""
        
    def replace_variable_in_params(self):
        # 如果参数中包含可变参数，从可变参数字典中读取并替换参数值
        # 替换域名，并取代理地址
        if "${host_qingdao}" in self.host:
            self.host = info.host_qingdao
        elif "${host_huanyou}" in self.host:
            self.host = info.host_huanyou
        elif "${host_yiqi}" in self.host:
            self.host = info.host_yiqi
        # self.proxies = json.loads(info.proxies)

        # 用例表中含host字符串的url，也需要走代理，如轨迹文件下载地址pass
        if self.host in self.url:
            pass
            # self.proxies = json.loads(info.proxies)

        # 替换接口参数中的可变参数
        if "${" in self.params:
            for keyword in const.var_dict:
                if self.params.find(keyword) >= 0:
                    if str(const.var_dict[keyword]) == '[]':
                        self.result = keyword + 'absent. Abort mission!'
                        return
                    else:
                        self.params = self.params.replace(keyword, str(const.var_dict[keyword]))
                        self.params = ' '.join(self.params.split())
            self.actual_params = self.params

        # 替换url中的可变参数
        elif "${" in self.url:
            for keyword in const.var_dict:
                if self.url.find(keyword) >= 0:
                    if str(const.var_dict[keyword]) == '[]':
                        self.result = keyword + 'absent. Abort mission!'
                        return
                    else:
                        self.url = self.url.replace(keyword, str(const.var_dict[keyword]))
        # print(const.var_dict)

        # 替换入参中的可变参数
        elif "result_${" in self.va_in_para:
            for keyword in const.var_dict:
                if self.va_in_para.find(keyword) >= 0:
                    if str(const.var_dict[keyword]) == '[]':
                        self.result = keyword + 'absent. Abort mission!'
                        return
                    else:
                        self.va_in_para = self.va_in_para.replace(keyword, str(const.var_dict[keyword]))
        
    def run_case(self):
        """报告需要的参数"""
        global ok, ng, case_list
        
        # 定义需要用到的参数
        global va_in_para
        va_in_para = self.va_in_para
        
        self.replace_variable_in_params()
        self.entire_url = self.host + self.url + "?" + self.params
        # logger.debug("\n ## 接口index{} ##:\t {}".format(self.num, self.entire_url))
        if "${" in self.entire_url:
            self.result = 'NA, 接口中有可变参数未替换'
            ng += 1
            return
        
        # 根据POST/GET方法不同，调用接口；调用异常或状态码不是200的，结果为fail
        try:
            if self.method == 'POST':
                self.response = requests.post(self.host + self.url, data=json.dumps(json.loads(self.params)))
                                              # , proxie=self.proxies)
                self.entire_url = self.host + self.url
            elif self.method == 'GET':
                self.response = requests.get(self.entire_url)
                # self.response = requests.get(self.entire_url, proxies=self.proxies)
            elif self.method == 'JSON':
                headers = {'Accept': 'application/json, text/plain, */*',
                           'Content-Type': 'application/json;charset=UTF-8'}
                self.response = requests.post(self.host + self.url, json=json.loads(self.params), headers=headers)
                # self.response = requests.post(self.host + self.url, json=json.loads(self.params), headers=headers,
                #                               proxies=self.proxies)
        except:
            self.result = 'Fail，请求失败'
            return
        self.code = self.response.status_code
        if self.response.status_code != 200:
            self.result = 'Fail，响应码非200'
        
        # 返回浮点数的四舍五入值
        self.elapsed = round(self.response.elapsed.total_seconds(), 3)
        self.response = self.response.text
        
        # 检查接口返回结果中是否包含检验项
        if "Fail" not in self.result:
            # 验证项为空
            if not self.checkpoint:
                self.result = 'Success'
            else:
                checkpoints = self.checkpoint.split("|")
                for checkpoint in checkpoints:
                    
                    # 去掉所有空格
                    checkpoint = "".join(checkpoint.split())
                    self.response = "".join(self.response.split())

                    if checkpoint in self.response:
                        self.result = 'Success'
                        break
                if self.result != 'Success':
                    self.fail_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    self.result = '响应结果不含：{}'.format(self.checkpoint)

        # logger.info("[执行结果][{}]".format(self.result))
        
        if self.result == 'Success':
            ok += 1
            self.result_value = 'Success'
            self.get_variable_value_from_result()
        else:
            ng += 1
            self.result_value = 'Fail'
            
        angle_list = []
        angle_list.append(self.num)
        angle_list.append(self.purpose)
        angle_list.append(self.method)
        angle_list.append(self.url)
        angle_list.append(self.result_value)
        angle_list.append(self.elapsed)
        angle_list.append(self.checkpoint)
        angle_list.append(self.code)
        angle_list.append(self.response.replace("<", "").replace(">", ""))
        case_list.append(angle_list)
        # return self
        
    # 从接口返回结果中解析关联数据，并存储到dict中
    # 如有多个关联数据，进行分割，得到数据如：${forumType}=[data][hotForumList][0][forumType]=
    def get_variable_value_from_result(self):
        # 可变参数想取多个值用;分割， 如：'${fleetName}=[data][mileageList][0][fleetName];${fleetName}=[data][oilList][1][fleetName]'
        var_list = self.variables.split(';')

        for var in var_list:
            param = var.split('=')
            if len(param) == 2:
                # 判断可变参数是否有效 为空，或者不是以[开头，或者以]结尾的
                if param[1] == '' or not re.search(r'^\[', param[1]) or not re.search(r'\]$', param[1]):
                    self.result = "关联参数设置错误"
                    continue
                response_js = json.loads(self.response)
                value = ""
                # 通过等号后的键值，逐步获得所指向的json串中的值
                for key in param[1][1:-1].split(']['):
                    # 随机选择list中的某个值。excel写法如：[random@5]
                    if 'random' in key:
                        key = random.randint(0, int(key.split('@')[1]))
                    # 按条件筛选值，如获取type为21的list值。excel写法如：[type:21]
                    elif ':' in key:
                        condition_key, condition_value = key.split(':')[0], key.split(':')[1]
                        for index in range(len(response_js)):
                            try:
                                if str(response_js[index][condition_key]) == condition_value:
                                    key = index
                                    break
                            except:
                                continue
                    # 通过键值获取结果中的相应字段值
                    try:
                        value = response_js[int(key)]
                    except:
                        try:
                            value = response_js[key]
                        except:
                            # 未找到时，传空值
                            value = None
                            break
                    response_js = value
                # 将关联参数和数值存到dict中
                if value is not None:
                    if param[0].find("-") != -1:
                        const.var_dict[''.join(str(param[0]).split())] = str(value - 1)
                    elif param[0].find("+") != -1:
                        const.var_dict[''.join(str(param[0]).split())] = str(value + 1)
                    else:
                        const.var_dict[''.join(str(param[0]).split())] = str(value)
                    # const.var_dict[str(param[0])] = str(value)
        pass

    def get_variable_in_params(self):
        """
        获取入参中的可变参数对应值
        :return:
        """
        if self.va_in_para:
            paraname = self.va_in_para
            return const.var_dict[paraname]


if __name__ == '__main__':
    print(str(False))
    che = "s"
    res = "ssss"
    if che in res:
        print("-----")
