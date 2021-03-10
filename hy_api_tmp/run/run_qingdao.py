# coding: utf-8
# !/usr/bin/python3
import sys, os

Base_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(Base_DIR)

from case import Excel
import login
import mail_new
import const
import time
import datetime
from LogUtils.logutil import LoggerUtil
import setting as info
import config.config_qingdao as q_con
# import config.config_yiqi as y_con

logger = LoggerUtil()

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class TestRunner:
    def __init__(self, project_name, env):
        self.env = env
        self.dir_case = root_path+"\\project\\{}.xls".format(project_name)
        self.dir_result = root_path+"\\project\\result/{}_{}/{}".format(project_name, env,
                                                                             time.strftime("%Y%m%d_%H%M%S"))
        if not os.path.isdir(self.dir_result):
            os.makedirs(self.dir_result)
            
        self.dir_case_result = root_path+"\\project/{}_result.xls".format(project_name)

    def run(self):
        const.start_time_style = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        const.start_time = datetime.datetime.now()
        # if self.env.lower() == "online" and info.iterm == "yiqi":
        #     # 先将token变量值写入字典
        #     const.var_dict["${token}"] = login.login(y_con.username_online_yiqi, y_con.password_online_yiqi, "GET")
        # elif self.env.lower() == "online" and info.iterm == "qingdao":
        #     const.var_dict["${token}"] = login.login(q_con.username_online_qingdao, q_con.password_online_qingdao, "GET")
        # else:
        #     const.var_dict["${token}"] = login.login(q_con.username, q_con.password, "GET")

        if self.env.lower() == "online" and info.iterm == "qingdao":
            const.var_dict["${token}"] = login.login(q_con.username_online_qingdao, q_con.password_online_qingdao, "GET")
        else:
            const.var_dict["${token}"] = login.login(q_con.username, q_con.password, "GET")
        
        excel = Excel(self.dir_case, self.dir_case_result)
       # html_report = htmlGenerator.report(self.dir_result)
        cases = excel.get_cases()
        for case in cases:
            # UAT环境，UAT一列，为No时不予执行
            if self.env.lower() == "uat":
                if case.uat_env != 'Yes':
                    continue

                case.run_case()
                if info.write_back == 0:
                    excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                    all_result = [case.entire_url, case.response, case.result_value, case.fail_time, case.elapsed,
                                  case.actual_params]
                    index = 0
                    for i in range(13, 19):
                        excel.set_out_cell(case.line, i, all_result[index])
                        excel.save_excel()
                        index += 1
                    excel.save_excel()
                    
                elif info.write_back == 1:
                    if case.result_value == 'Fail':
                        excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                        all_result = [case.entire_url, case.response, case.result_value, case.fail_time, case.elapsed, case.actual_params]
                        index = 0
                        for i in range(13, 19):
                            excel.set_out_cell(case.line, i, all_result[index])
                            excel.save_excel()
                            index += 1
                    excel.save_excel()

                # html_report.add_case(case)
            
            # Test环境，Test一列，为No时不予执行
            if self.env.lower() == "test":
                if case.test_env != 'Yes':
                    continue
                case.run_case()
                if info.write_back == 0:
                    excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                    all_result = [case.entire_url, case.response, case.result_value, case.fail_time, case.elapsed, case.actual_params]
                    index = 0
                    for i in range(13, 19):
                        excel.set_out_cell(case.line, i, all_result[index])
                        excel.save_excel()
                        index += 1
                    excel.save_excel()
                elif info.write_back == 1:
                    if case.result_value == 'Fail':
                        excel.set_out_cell(excel.ROW_G, 9,
                                           '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                        all_result = [case.entire_url, case.response, case.result_value, case.fail_time, case.elapsed,
                                      case.actual_params]
                        index = 0
                        for i in range(13, 19):
                            excel.set_out_cell(case.line, i, all_result[index])
                            excel.save_excel()
                            index += 1
                    excel.save_excel()
                
            # online 环境，Test一列，为No时不予执行
            if self.env.lower() == "online":
                if case.online_env != 'Yes':
                    continue
                case.run_case()
                if info.write_back == 0:
                    excel.set_out_cell(excel.ROW_G, 9, '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                    all_result = [case.entire_url, case.response, case.result_value]
                    index = 0
                    for i in range(13, 16):
                        excel.set_out_cell(case.line, i, all_result[index])
                        excel.save_excel()
                        index += 1
                    excel.save_excel()
                # html_report.add_case(case)
                elif info.write_back == 1:
                    if case.result_value == 'Fail':
                        excel.set_out_cell(excel.ROW_G, 9,
                                           '{}={}'.format(case.va_in_para, case.get_variable_in_params()))
                        all_result = [case.entire_url, case.response, case.result_value]
                        index = 0
                        for i in range(13, 16):
                            excel.set_out_cell(case.line, i, all_result[index])
                            excel.save_excel()
                            index += 1
                    excel.save_excel()
            
        excel.color_execl(self.dir_case_result)

        const.end_time_style = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        const.end_time = datetime.datetime.now()
        const.total_time = (const.end_time-const.start_time).seconds
        # login.logout(self.cfg, const.var_dict["${token}"])
        
    def send_mail(self):
        mail_new.SendReport()

        
def main():
    info.project_name = q_con.project_name
    project_name = info.project_name

    info.env = q_con.env
    env = info.env.lower()

    info.title = q_con.title
    info.iterm = q_con.iterm

    info.Form = q_con.Form
    info.pw = q_con.pw
    info.server = q_con.server
    info.To = q_con.To
    info.send_email = q_con.send_email

    # info.project_name = os.environ["excel_name"]  # q_con.project_name
    # project_name = info.project_name
    #
    # info.env = os.environ["run_environment"]  # q_con.env
    # env = info.env.lower()
    #
    # info.title = os.environ["report_title"]  # q_con.title
    # info.iterm = q_con.iterm
    #
    # info.Form = q_con.Form
    # info.pw = q_con.pw
    # info.server = q_con.server
    # info.To = os.environ["mail_receiver"]    # q_con.To
    # info.send_email = os.environ["send_mail"]  # q_con.send_email
    
    if env == "test":
        info.host_qingdao = q_con.test_host_qingdao
        info.host_huanyou = info.test_host_huanyou
    elif env == "uat":
        info.host_qingdao = q_con.uat_host_qingdao
        info.host_huanyou = info.uat_host_huanyou
    elif env == "online":
        info.host_qingdao = q_con.online_host_qingdao
        info.proxies = info.online_proxies
        
    # 执行单元测试
    test_runner = TestRunner(project_name, env)
    test_runner.run()
    test_runner.send_mail()


if __name__ == '__main__':
    main()