# coding: utf-8
import requests
import json
import random

import hashlib
from LogUtils.logutil import LoggerUtil
logger = LoggerUtil()


def getVerifyCodeId():
    str = []
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(16):
        str.append(random.choice(arr))
    return "".join(str)


def login(cfg):
    url = "{}/driver/login".format(cfg.getConfig("host"))
    username = cfg.getConfig("username")
    password = cfg.getConfig("password")
    logger.info("用户登录成功,账号[{}] && 密码[{}]".format(username, password))
    
    if cfg.getConfig("md5") == "true":
        password = hashlib.md5(password.encode('utf8')).hexdigest()

    params = {"loginName": username,
              "password": password,
              "deviceId": "F30E1387 - 5127 - 4515 - A876 - DC1A05C6B5A2",
              "product": "qingqi",
              "deviceType": "2",
              "version": "1.19.1",
              "appType": "qingqi_owner_mobile"
              }
    r = requests.post(url, data=json.dumps(params), proxies=json.loads(cfg.getConfig("proxies")))

    result = r.json()
    logger.info("登录接口返回的结果\n {}".format(result))
    return result["data"]["token"]


def logout(cfg, token):
    url = "{}/authority/logout?token={}".format(cfg.getConfig("host"), token)
    requests.get(url, proxies=json.loads(cfg.getConfig("proxies")))

