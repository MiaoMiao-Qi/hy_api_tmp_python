# coding: utf-8
from case import Excel
import sys
import os
import login
import mail_new
import const
import time
import datetime
from LogUtils.logutil import LoggerUtil
import setting as info

logger = LoggerUtil()

root_path = os.path.abspath(os.path.dirname(__file__))


class TestRunner:
    def __init__(self, project_name, env):
        self.env = env
        self.dir_case = root_path+"project\\{}.xls".format(project_name)
        print("当前执行目录====",self.dir_case)
        self.dir_result = os.path.join(os.getcwd(), "result/{}_{}/{}".format(project_name, env,
                                                                             time.strftime("%Y%m%d_%H%M%S")))
        if not os.path.isdir(self.dir_result):
            os.makedirs(self.dir_result)
        self.dir_case_result = os.path.join(os.getcwd(), "project/{}_result.xls".format(project_name))

    def run(self):
        const.start_time_style = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        const.start_time = datetime.datetime.now()
        
        # 先将token变量值写入字典
        const.var_dict["${token}"] = login.login(info.username, info.password, "GET")

        excel = Excel(self.dir_case, self.dir_case_result)
       # html_report = htmlGenerator.report(self.dir_result)
        cases = excel.get_cases()
        for case in cases:
            # UAT环境，UAT一列，为No时不予执行
            if self.env.lower() == "uat":
                if case.uat_env == 'No':
                    continue

                case.run_case()
                excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                all_result = [case.entire_url, case.response, case.result_value]
                index = 0
                for i in range(13, 16):
                    excel.set_out_cell(case.line, i, all_result[index])
                    excel.save_excel()
                    index += 1
                excel.save_excel()

                # html_report.add_case(case)
            
            # Test环境，Test一列，为No时不予执行
            if self.env.lower() == "test":
                if case.test_env == 'No':
                    continue
                case.run_case()
                excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                all_result = [case.entire_url, case.response, case.result_value]
                index = 0
                for i in range(13, 16):
                    excel.set_out_cell(case.line, i, all_result[index])
                    excel.save_excel()
                    index += 1
                excel.save_excel()
                
            # online 环境，Test一列，为No时不予执行
            if self.env.lower() == "online":
                if case.test_env == 'No':
                    continue
                case.run_case()
                excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                all_result = [case.entire_url, case.response, case.result_value]
                index = 0
                for i in range(13, 16):
                    excel.set_out_cell(case.line, i, all_result[index])
                    excel.save_excel()
                    index += 1
                excel.save_excel()
                # html_report.add_case(case)

        excel.color_execl(self.dir_case_result)

        const.end_time_style = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        const.end_time = datetime.datetime.now()
        const.total_time = (const.end_time-const.start_time).seconds
        # login.logout(self.cfg, const.var_dict["${token}"])
        
    def send_mail(self):
        mail_new.SendReport()

        
def main():
    project_name = info.project_name
    env = info.env.lower()
    if env == "test":
        info.host_qingdao = info.test_host_qingdao
        info.host_huanyou = info.test_host_huanyou
        info.proxies = info.test_proxies
    elif env == "uat":
        info.host_qingdao = info.uat_host_qingdao
        info.host_huanyou = info.uat_host_huanyou
        info.proxies = info.uat_proxies
    elif env == "online":
        info.host = info.online_host
        info.proxies = info.online_proxies
        
    # 执行单元测试
    test_runner = TestRunner(project_name, env)
    test_runner.run()
    test_runner.send_mail()


if __name__ == '__main__':
    main()