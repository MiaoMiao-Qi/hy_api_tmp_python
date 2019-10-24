#-*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# Name:        const
# Purpose:
#
# Author:      liuhuan3
#
# Created:     24/04/2017
# Copyright:   (c) liuhuan3 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import datetime

# 定义初始的关联参数列表
var_dict = {}
var_dict["${token}"] = ''   # 账号登录成功后传入该值
var_dict["${currentMonth}"] = time.strftime("%Y-%m")
var_dict["${currentDay}"] = time.strftime("%Y%m%d")
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

var_dict["${timestamp_now}"] = int(time.time())*1000

var_dict["${HHHHH}"] = lastYear.strftime("%Y-%m-%d")
