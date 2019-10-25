# coding: utf-8
from case import Excel
import htmlGenerator  
import sys
import os
import login
from config import Config
import mail
import const
import time
from LogUtils.logutil import LoggerUtil

logger = LoggerUtil()


class TestRunner:
    def __init__(self, cfg, project_name, env):
        self.cfg = cfg
        self.env = env
        self.dir_case = os.path.join(os.getcwd(), "project/api_{}.xls".format(project_name))
        self.dir_result = os.path.join(os.getcwd(), "result/{}_{}/{}".format(project_name, env, time.strftime("%Y%m%d_%H%M%S")))
        if not os.path.isdir(self.dir_result):
            os.makedirs(self.dir_result)

    def run(self):
        # 先将token变量值写入字典
        const.var_dict["${token}"] = login.login(self.cfg)

        excel = Excel(self.dir_case, self.cfg)
        html_report = htmlGenerator.report(self.dir_result)
        cases = excel.get_cases()
        for case in cases:
            # 线上运行时，online属性为No的不予执行
            if self.env.lower() == 'online':
                if case.active_online == 'No':
                    continue
            # # 非线上环境，未激活接口不予执行
            # else:
            #     if case.active == 'No':
            #         continue
            
            # UAT环境，UAT一列，为No时不予执行
            if self.env.lower() == "uat":
                if case.uat_env == 'No':
                    continue
                    
            # Test环境，Test一列，为No时不予执行
            if self.env.lower() == "test":
                if case.test_env == 'No':
                    continue
            
            case.run_case()
            html_report.add_case(case)

            # time.sleep(5)

        login.logout(self.cfg, const.var_dict["${token}"])

    def send_mail(self):
        mail.send_mail(self.cfg, self.dir_result)


def main():
    project = 'dongfengCAPP-UAT'
    # 读取命令行参数
    if len(sys.argv) > 1:
        project = sys.argv[1]
    # 读取配置文件
    cfg = Config('config/{}'.format(project))

    project_name = project.split("-")[0]
    env = project.split("-")[1]
    logger.info("当前配置项{}".format(project_name))

    # 执行单元测试
    test_runner = TestRunner(cfg, project_name, env)
    test_runner.run()
    test_runner.send_mail()


if __name__ == '__main__':
    main()