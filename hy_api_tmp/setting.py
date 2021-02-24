# 环境 线上online  UAT环境uat 测试环境test
env = "online"

# 项目名称 一汽项目 yiqi 青汽项目 qingdao 环游项目 huanyou
iterm = "yiqi"

# 报告名称 #"青岛_TBOSS_销售可视化_Main" "一汽_TBOSS_Sanity" "一汽_TBOSS_Sanity线上"
title = "一汽_TBOSS_Sanity"

# 接口用例excel名称 "TBOSS_qingdao_sale"  "TBOSS_yiqi" 线上环境 TBOSS_yiqi_online
project_name = "TBOSS_yiqi_online"

# 是否发送邮件 True发送邮件 False不发送邮件
send_email = False

# 结果是否回写到excel中 0结果全部回写 1只回写失败的接口
write_back = 1


# 用户名(青岛和一汽同名)
username = "testInter"
username_online_yiqi = "yaochangyu"   # Yaochangyu@2020
password_online_yiqi = "fwIJSqLdDoXQAjKS4TmROA%3D%3D"

username_online_qingdao = "systemcontrol"
password_online_qingdao = "Aa147258@"

# 密码
# password=Aa%13579
password = "ehmL%2FsPnR5sKW3i7vSASzQ%3D%3D"
md5 = "false"

host_qingdao = ''
host_yiqi = ''
host_huanyou = ''

# 青岛Tboss host地址
test_host_qingdao = 'http://sy.aerozhonghuan.com:81/test/yiqi/web/qdfaw/yiqiTbossParallel/#/home'
uat_host_qingdao = 'https://uat-iov-ec.fawjiefang.com.cn/app/api/'
test_proxies = '{"http": "http://211.145.49.132:81"}'
online_host_qingdao = 'https://iov-tboss.fawjiefang.com.cn/tboss/'

# 一汽Tboss host地址
test_host_yiqi = 'http://sy.aerozhonghuan.com:81/test/yiqi/app/api/'
uat_host_yiqi = 'https://uat-iov-ec.fawjiefang.com.cn/app/api/'
online_host_yiqi = 'https://iov-ec.fawjiefang.com.cn/app/api/'

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
Form = 'aototest@smartlink-tech.com.cn'
pw = 'Aa20202020'
server = 'smtphz.qiye.163.com'
To = "jiyanjiao@smartlink-tech.com.cn"
# To = "jiyanjiao@smartlink-tech.com.cn,weijie@smartlink-tech.com.cn,wangqi@smartlink-tech.com.cn,houqingxuan@smartlink-tech.com.cn"
