# 环境 线上online  UAT环境uat 测试环境test
env = ""

# 项目名称 一汽项目 yiqi 青汽项目 qingdao 环游项目 huanyou
iterm = ""

# 报告名称 #"青岛_TBOSS_销售可视化_Main" "一汽_TBOSS_Sanity" "一汽_TBOSS_Sanity_线上" "青岛_TBOSS_Sanity_线上"
title = ""

# 接口用例excel名称 "TBOSS_qingdao_sale"  "TBOSS_yiqi" 线上环境 TBOSS_yiqi_online TBOSS_qingdao_online TBOSS_qingdao_online
project_name = ""

# 是否发送邮件 True发送邮件 False不发送邮件
send_email = True

# 结果是否回写到excel中 0结果全部回写 1只回写失败的接口
write_back = 0

md5 = "false"

host_qingdao = ''
host_yiqi = ''
host_huanyou = ''

# 寰游 host地址
test_host_huanyou = ""
uat_host_huanyou = "https://cc.aerohuanyou.com/api/qingqi/"
uat_proxies = '{"http": "http://211.145.49.132:81"}'


# 司机车队青岛 host地址
dev_dm_host_qingdao = "https://cc.aerohuanyou.com/dev/yiqi/app/api/"
test_dm_host_qingdao = "https://cc.aerohuanyou.com/test/yiqi/app/api/"
uat_dm_host_qingdao = "https://uat-iov-ec.fawjiefang.com.cn/app/api"

# 司机车队一汽 host地址
dev_dm_host_changchun = "https://cc.aerohuanyou.com/dev/yiqi/app/api/"
test_dm_host_chanchun = "https://cc.aerohuanyou.com/test/yiqi/app/api/"
uat_dm_host_changchun = "https://uat-iov-ec.fawjiefang.com.cn/app/api/"


online_host = ''
online_proxies = ''

"""邮箱发送 配置"""
Form = ''
pw = ''
server = ''
# To = "jiyanjiao@smartlink-tech.com.cn"
To = ""
