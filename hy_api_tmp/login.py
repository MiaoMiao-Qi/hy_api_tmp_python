# coding: utf-8
import requests
import json
import random

import hashlib
import setting as info
from LogUtils.logutil import LoggerUtil
logger = LoggerUtil()


def getVerifyCodeId():
    str = []
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(16):
        str.append(random.choice(arr))
    return "".join(str)


def login(username, password, method):
    """
    获取token的方法
    :param username:
    :param password:
    :param method:
    :return:
    """
    url = "{}faw/operate/login".format(info.host_qingdao)
    # logger.info("用户登录成功,账号[{}] && 密码[{}]".format(username, password))
    
    if info.md5 == "true":
        password = hashlib.md5(password.encode('utf8')).hexdigest()
    if method == "POST":
        params = {"loginName": username,
                  "password": password,
                  "deviceId": "F30E1387 - 5127 - 4515 - A876 - DC1A05C6B5A2",
                  "product": "qingqi",
                  "deviceType": "2",
                  "version": "1.19.1",
                  "appType": "qingqi_owner_mobile"
                  }
        # 转换成json格式 data=json.dumps(params)
        # http请求走http对应的地址, https请求走https对应的地址,在请求中加入了一个proxies的参数
        # proxies参数代理是一个字典
        response = requests.post(url, data=json.dumps(params)) #, proxies=json.loads(cfg.getConfig("proxies")))
        
    elif method == "GET":
        data = "?loginName={}&loginPwd={}".format(username, password)
        response = requests.request(method, url+data)
    try:
        result = response.json()
        logger.info("登录接口返回的结果\n {}".format(result))
        return result["data"]["token"]
    except Exception as e:
        print("登陆接口出现异常", e)


def logout(cfg, token):
    url = "{}/authority/logout?token={}".format(cfg.getConfig("host"), token)
    requests.get(url, proxies=json.loads(cfg.getConfig("proxies")))

