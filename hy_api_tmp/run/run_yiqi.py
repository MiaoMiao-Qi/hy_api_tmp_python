# coding: utf-8
from case import Excel
import os
import login
import mail_new
import const
import time
import datetime
from LogUtils.logutil import LoggerUtil
import setting as info
# import config.config_qingdao as y_con
import config.config_yiqi as y_con

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
        #     const.var_dict["${token}"] = login.login(y_con.username_online_qingdao, y_con.password_online_qingdao, "GET")
        # else:
        #     const.var_dict["${token}"] = login.login(y_con.username, y_con.password, "GET")
        
        if self.env.lower() == "online" and info.iterm == "yiqi":
            const.var_dict["${token}"] = login.login(y_con.username_online_yiqi, y_con.password_online_yiqi, "GET")
        else:
            const.var_dict["${token}"] = login.login(y_con.username, y_con.password, "GET")

        excel = Excel(self.dir_case, self.dir_case_result)
       # html_report = htmlGenerator.report(self.dir_result)
        cases = excel.get_cases()
        for case in cases:
            # UAT环境，UAT一列，为No时不予执行
            if self.env.lower() == "uat":
                if case.uat_env == 'No':
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
                if case.test_env == 'No':
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
                if case.online_env == 'No':
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
    info.project_name = y_con.project_name
    project_name = info.project_name
    
    info.env = y_con.env
    env = info.env.lower()
    
    info.title = y_con.title
    info.iterm = y_con.iterm
    
    info.Form = y_con.Form
    info.pw = y_con.pw
    info.server = y_con.server
    info.To = y_con.To
    info.send_email = y_con.send_email
    
    if env == "test":
        info.host_huanyou = info.test_host_huanyou
        info.host_yiqi = y_con.test_host_yiqi
    elif env == "uat":
        info.host_huanyou = info.uat_host_huanyou
        info.host_yiqi = y_con.uat_host_yiqi
        info.proxies = info.uat_proxies
    elif env == "online":
        info.host_yiqi = y_con.online_host_yiqi
        info.proxies = info.online_proxies
        
    # 执行单元测试
    test_runner = TestRunner(project_name, env)
    test_runner.run()
    test_runner.send_mail()


if __name__ == '__main__':
    main()