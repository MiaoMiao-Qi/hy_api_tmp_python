
from html3.html3 import HTML
import os


class report:
    def __init__(self, dir_result):
        # 获取响应结果保存路径
        self.path_html_report = "{}/api_testResult.html".format(dir_result)
        self.path_log = "{}/log".format(dir_result)

        self.page = HTML()
        self.page.title("API Test Result")
        # #d0d0d0 灰色 #008000 绿色 #8E8E8E 	#4682B4蓝色
        self.table = self.page.table(border="3", cellSpacing="0", width="90%", borderColor="#d0d0d0")
        r = self.table.tr(bgcolor="#4682B4")
        r.td("编号")
        r.td("模块")
        r.td("接口")
        r.td("Get/Post")
        r.td("验证字符串")
        r.td("运行结果")
        r.td("运行时间(s)")
        r.td("详细结果")

        self.save_page(str(self.page))

    # 保存html页面
    def save_page(self, content):
        htmlFile = open(self.path_html_report, "w")
        # print(content)
        htmlFile.write(content)
        htmlFile.close()

    # 将case运行结果添加到html报告中
    def add_case(self, case):
        r = self.table.tr()
        r.td(str(case.num))
        r.td(case.module)
        r.td.a(case.purpose, href=case.entire_url)
        r.td(case.method)
        r.td(str(case.checkpoint))
        if case.result != "Success":
            r.td(case.result, bgcolor="#F3bf88")     # 黄色
        else:
            r.td(case.result)
      
        if case.elapsed == 'null' or case.elapsed == '':
            pass
        elif float(case.elapsed) > 5:
            r.td(str(case.elapsed), bgcolor="#Fef263")  # 亮黄色
        else:
            r.td(str(case.elapsed))

        # 将接口response文件链接加到结果中
        if case.response:
            path_response = self.save_response(case)
            r.td.a("响应结果", href=path_response)

        self.save_page(str(self.page))

    # 将接口response数据保存到txt中
    def save_response(self, case):
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)

        path_response = os.path.join(self.path_log, "%d.txt" % case.num)
        logFile = open(path_response, "w")

        # 非表格形式的相应结果，写入结果文件中
        if ".xlsm" not in case.entire_url:
            if len(case.response) > 30000:
                case.response = case.response[0:30000]
            logFile.write(case.response)
            logFile.close()

        return "log/%d.txt" % case.num

