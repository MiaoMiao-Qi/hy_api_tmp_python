# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import re
from config import Config


def send_mail(cfg, dir_result):
    msg = MIMEMultipart()

    #  添加附件：report.html
    att1 = MIMEText(open("{}/api_testResult.html".format(dir_result), 'rb').read(), 'plain', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "report.html"))
    msg.attach(att1)

    # 添加附件：截图、日志等打包后的文件
    add_zip(dir_result)
    att2 = MIMEText(open("report.zip", 'rb').read(), 'plain', 'utf-8')
    att2['Content-Type'] = 'application/octet-stream'
    att2.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "详细测试报告.zip"))
    msg.attach(att2)

    # 邮件内容
    msg.attach(MIMEText(get_mail_content(dir_result), 'plain', 'utf-8'))
    msg['Subject'] = cfg.getConfig("mail_title")
    msg['From'] = cfg.getConfig("mail_sender")
    msg['To'] = cfg.getConfig("mail_recv")

    smtp = smtplib.SMTP(cfg.getConfig("mail_server"))
    smtp.login(cfg.getConfig("mail_sender"), cfg.getConfig("mail_sender_pwd"))

    try:
        smtp.sendmail(cfg.getConfig("mail_sender"), cfg.getConfig("mail_recv").split(','), msg.as_string())
    except Exception as e:
        print('出错了。。', e)
    else:
        print('发送成功！')

    smtp.quit()


def add_zip(dir_result):
    shutil.make_archive('report', 'zip', dir_result)

def get_mail_content(dir_result):
    result_file = open("{}/api_testResult.html".format(dir_result)).read()

    total_num = len(re.findall("http:", result_file))
    pass_num = len(re.findall("<td>Success</td>", result_file))
    return "大家好！\n" \
           "此报告为自动发送，本次用例执行情况如下：\n" \
           "用例总数: {} \n " \
           "通过用例:  {} \n" \
           "失败用例:   {} \n\n" \
           "如需查看详细接口调用情况，请解压附件中的zip包进行查看，谢谢！" .format(total_num, pass_num, total_num-pass_num)

if __name__ == '__main__':
    cfg = Config('config/{}'.format("cddy-test"))
    send_mail(cfg, "D:\\code\\HY_API_excel\\result\\cddy_test\\20190313_091743")
    # add_zip("./result")
    # pass
