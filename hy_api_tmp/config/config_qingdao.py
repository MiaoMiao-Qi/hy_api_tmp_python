# 青岛Tboss host地址
test_host_qingdao = 'http://sy.aerozhonghuan.com:81/test/yiqi/web/qdfaw/yiqiTbossParallel/#/home'
uat_host_qingdao = 'https://uat-iov-ec.fawjiefang.com.cn/app/api/'
test_proxies = '{"http": "http://211.145.49.132:81"}'
online_host_qingdao = 'https://iov-ec.fawjiefang.com.cn/app/api/'


username = "testInter"
password = "ehmL%2FsPnR5sKW3i7vSASzQ%3D%3D"

username_online_qingdao = "systemcontrol"
password_online_qingdao = "q5EkYtLaxBppzW68isps2Q%3D%3D"  # "Aa147258@"

# 环境 线上online  UAT环境uat 测试环境test
env = "uat"

# 项目名称 一汽项目 yiqi 青汽项目 qingdao 环游项目 huanyou
iterm = "qingdao"

# 报告名称 #"青岛_TBOSS_销售可视化_Main" "一汽_TBOSS_Sanity" "一汽_TBOSS_Sanity_线上" "青岛_TBOSS_Sanity_线上"
title = "青岛_TBOSS_Sanity_uat"

# 接口用例excel名称 "TBOSS_qingdao_sale"  "TBOSS_yiqi" 线上环境 TBOSS_yiqi_online TBOSS_qingdao_online TBOSS_qingdao_online
project_name = "TBOSS_qingdao_uat1"

# 是否发送邮件 True发送邮件 False不发送邮件
send_email = True
# 结果是否回写到excel中 0结果全部回写 1只回写失败的接口
write_back = 1

"""邮箱发送 配置"""
Form = 'aototest@smartlink-tech.com.cn'
pw = 'Aa20202020'
server = 'smtphz.qiye.163.com'
To = "wangqi@smartlink-tech.com.cn"
# To = "jiyanjiao@smartlink-tech.com.cn,weijie@smartlink-tech.com.cn,wangqi@smartlink-tech.com.cn,houqingxuan@smartlink-tech.com.cn"