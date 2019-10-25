# coding: utf-8
# Purpose：接口自动化测试
# Author：Liu huan
# 参考Blog：http://www.bstester.com/2015/08/interface-test-automation-scheme-details

import json
import re
import os
import sys
import xlrd
import requests
import random
import const
from LogUtils.logutil import LoggerUtil
logger = LoggerUtil()


class Excel:
    def __init__(self, path, cfg):
        print('==========================='+path)
        if not os.path.exists(path):
            print('测试用例文件不存在！！！')
            sys.exit()
        self.api_file = xlrd.open_workbook(path)
        self.api_sheet = self.api_file.sheet_by_index(0)

        self.cases = []
        self.cfg = cfg

    def get_cases(self):
        # 读取excel中每一行的值
        for line in range(1, self.api_sheet.nrows):
            case = Case(self.cfg)
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
            # 读的是Test列
            # case.active = self.api_sheet.cell(line, 9).value.replace('\n', '').replace('\r', '')
            # # 读的是UAT列
            # case.active_online = self.api_sheet.cell(line, 10).value.replace('\n', '').replace('\r', '')

            case.uat_env = self.api_sheet.cell(line, 10).value.replace('\n', '').replace('\r', '')
            case.test_env = self.api_sheet.cell(line, 9).value.replace('\n', '').replace('\r', '')
            self.cases.append(case)
        return self.cases


class Case:
    def __init__(self, cfg):
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
        self.cfg = cfg
        self.proxies = {}
        self.elapsed = ""
        
        self.uat_env = "No"
        self.test_env = 'No'

    def replace_variable_in_params(self):
        # 如果参数中包含可变参数，从可变参数字典中读取并替换参数值
        # 替换域名，并取代理地址
        if "${host}" in self.host:
            self.host = self.cfg.getConfig("host")
            self.proxies = json.loads(self.cfg.getConfig("proxies"))

        # 用例表中含host字符串的url，也需要走代理，如轨迹文件下载地址
        if self.host in self.url:
            self.proxies = json.loads(self.cfg.getConfig("proxies"))

        # 替换接口参数中的可变参数
        if "${" in self.params:
            for keyword in const.var_dict:
                if self.params.find(keyword) >= 0:
                    if str(const.var_dict[keyword]) == '[]':
                        self.result = keyword + 'absent. Abort mission!'
                        return
                    else:
                        self.params = self.params.replace(keyword, str(const.var_dict[keyword]))

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

    def run_case(self):
        self.replace_variable_in_params()
        self.entire_url = self.host + self.url + "?" + self.params
        logger.debug\
            ("\n ## 接口index{} ##:\t {}".format(self.num, self.entire_url))
        # print("Index:%d:\t%s" % (self.num, self.entire_url))
        if "${" in self.entire_url:
            self.result = 'NA, 接口中有可变参数未替换'
            return

        # 根据POST/GET方法不同，调用接口；调用异常或状态码不是200的，结果为fail
        try:
            if self.method == 'POST':
                self.response = requests.post(self.host + self.url, data=json.dumps(json.loads(self.params)), proxies=self.proxies)
            elif self.method == 'GET':
                self.response = requests.get(self.entire_url, proxies=self.proxies)
            elif self.method == 'JSON':
                headers = {'Accept': 'application/json, text/plain, */*',
                           'Content-Type': 'application/json;charset=UTF-8'}
                self.response = requests.post(self.host + self.url, json=json.loads(self.params), headers = headers,
                                              proxies=self.proxies)
        except:
            self.result = 'Fail，请求失败'
            return
        if self.response.status_code != 200:
            self.result = 'Fail，响应码非200'

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

                    if checkpoint in self.response:
                        self.result = 'Success'
                        break
                if self.result != 'Success':
                    self.result = '响应结果不含：{}'.format(self.checkpoint)

        # print(self.result)
        logger.info("[执行结果][{}]".format(self.result))
        if self.result == 'Success':
            self.get_variable_value_from_result()
        # return self

    # 从接口返回结果中解析关联数据，并存储到dict中
    # 如有多个关联数据，进行分割，得到数据如：${forumType}=[data][hotForumList][0][forumType]
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
                    const.var_dict[str(param[0])] = str(value)
                    

if __name__ == '__main__':
    print(str(False))
    che = "s"
    res = "ssss"
    if che in res:
        print("-----")
