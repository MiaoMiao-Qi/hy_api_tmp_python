import time
import datetime
from Utils.stringutil import StringUtil as util
import random

# 定义初始的关联参数列表
var_dict = dict()
var_dict["${token}"] = ''   # 账号登录成功后传入该值
var_dict["${currentMonth}"] = time.strftime("%Y-%m")
var_dict["${currentDay}"] = time.strftime("%Y-%m-%d")
var_dict["${currentDay_num}"] = time.strftime("%Y%m%d")
var_dict["${currentTime}"] = time.strftime("%Y-%m-%d %H:%M:%S")

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
lastWeek = datetime.datetime.now() - datetime.timedelta(days=7)
lastMonth = datetime.datetime.now() - datetime.timedelta(days=30)
lastYear = datetime.datetime.now() - datetime.timedelta(days=366)
var_dict["${yesterday}"] = yesterday.strftime("%Y-%m-%d")
var_dict["${lastWeek}"] = lastWeek.strftime("%Y-%m-%d")
var_dict["${lastMonth_day}"] = lastMonth.strftime("%Y-%m-%d")
var_dict["${lastMonth}"] = lastMonth.strftime("%Y-%m")
var_dict["${lastYear_day}"] = lastYear.strftime("%Y-%m-%d")

start_time_style = None
start_time = None
end_time = None
end_time_style = None
total_time = 0

var_dict["${timestamp_now}"] = int(time.time())*1000

var_dict["${HHHHH}"] = lastYear.strftime("%Y-%m-%d")
var_dict["${random_num}"] = time.strftime("%H%M%S", time.localtime())
var_dict["result_${random_num}"] = ''
var_dict["${telephone}"] = util.random_phone_number(1)[0]



