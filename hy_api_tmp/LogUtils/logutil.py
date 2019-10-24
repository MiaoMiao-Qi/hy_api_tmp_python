
# coding: utf-8
# Purpose：log工具
# Author：jiyanjiao 2019-8-8

import logging
import os
import shutil
import sys
import time
from colorama import Fore, Style
from LogUtils.configutil import ConfigParser


class LoggerUtil:
    """log工具类"""
    # 获取当前工程的路径
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 配置文件的路径
    ini_path = project_path + "\\logUtils\\config.ini"
    # Log存放的路径
    log_path = project_path + "\\Logs\\"
    
    def __new__(cls):
        # 判断属性是否存在
        if hasattr(cls, "ins"):
            return cls.ins
        # 不存在就创建对象（保证无论实例几次均只有一个对象）
        cls.ins = super(LoggerUtil, cls).__new__(cls)
        # logger的一些初始设置
        LoggerUtil.init_instance(cls.ins)
        
        ins = cls.ins
        # 返回这个对象
        return ins
    
    def __init__(self):
        pass
    
    @staticmethod
    def init_instance(ins):
        # 清除log文件
        LoggerUtil.clear_log_file_path(ins)
        # 创建log路径
        LoggerUtil.create_log_path(ins)
        # 设置log类型
        LoggerUtil.set_logger_type(ins)
    
    @staticmethod
    def clear_log_file_path(ins):
        if ins.is_exists(LoggerUtil.log_path):
            ins.clear_data(LoggerUtil.log_path)
    
    @staticmethod
    def set_consle_logger(ins):
        # 控制台输出日志
        ins.consle = logging.StreamHandler()
        ins.file_logger.addHandler(ins.consle)
    
    @staticmethod
    def set_logger_type(ins):
        # 设置log输出格式
        ins.logger = logging.getLogger("log_in_file")
        # 对输出格式化进行了重新定义(fileName), methodName, lineNo
        ins.formatter = logging.Formatter('%(asctime)s - %(fileName)s - %(methodName)s - %(lineNo)s - %(message)s')
        # ' %(levelname)s - %(message)s')
        
        if LoggerUtil.read_config("log_type") == '1':
            # 1 文件输出
            LoggerUtil.log_in_file(ins)
        elif LoggerUtil.read_config("log_type") == '2':
            # 2 控制台输出
            LoggerUtil.log_in_consle(ins)
        elif LoggerUtil.read_config("log_type") == '3':
            # 3 控制台与文件均输出
            LoggerUtil.log_in_file(ins)
            LoggerUtil.log_in_consle(ins)
    
    @staticmethod
    def log_in_file(ins):
        # 文件输出
        ins.file_handle = logging.FileHandler(ins.log_file, 'a', encoding='utf-8')
        ins.file_handle.setFormatter(ins.formatter)
        
        # 指定最低的日志级别 critical > error > warning > info > debug
        ins.logger.setLevel(logging.DEBUG)
        ins.logger.addHandler(ins.file_handle)
    
    @staticmethod
    def log_in_consle(ins):
        # 控制台输出
        # 指定最低的日志级别 critical > error > warning > info > debug
        ins.logger.setLevel(logging.DEBUG)
        ins.consle_handler = logging.StreamHandler()
        ins.consle_handler.setFormatter(ins.formatter)
        ins.logger.addHandler(ins.consle_handler)
    
    @staticmethod
    def create_log_path(ins):
        # log存放路径
        if not LoggerUtil.is_exists(LoggerUtil.log_path):
            LoggerUtil.mik_dirs(LoggerUtil.log_path)
        # log存放名称
        ins.log_file = LoggerUtil.log_path + "{}.{}".format(time.strftime("%Y-%m-%d", time.localtime()), 'log')
        LoggerUtil.mik_file(ins.log_file)
    
    @staticmethod
    def debug(msg):
        # 对输出格式化进行了定义
        # Fore 定义输出的颜色debug - -white，info - -green，warning / error / critical - -red
        LoggerUtil.ins.logger.setLevel(logging.DEBUG)
        LoggerUtil.ins.logger.debug(Fore.WHITE + 'DEBUG - ' + msg + Style.RESET_ALL,
                                    extra={'fileName': LoggerUtil._findCaller()[0],
                                           'methodName': LoggerUtil._findCaller()[2],
                                           'lineNo': LoggerUtil._findCaller()[1]})
    
    @staticmethod
    def info(msg):
        LoggerUtil.ins.logger.setLevel(logging.INFO)
        LoggerUtil.ins.logger.info(Fore.GREEN + 'INFO - ' + msg,
                                   extra={'fileName': LoggerUtil._findCaller()[0],
                                          'methodName': LoggerUtil._findCaller()[2],
                                          'lineNo': LoggerUtil._findCaller()[1]})
    
    @staticmethod
    def error(msg):
        LoggerUtil.ins.logger.setLevel(logging.ERROR)
        LoggerUtil.ins.logger.error(Fore.RED + 'ERROR : \n' + msg,
                                    extra={'fileName': LoggerUtil._findCaller()[0],
                                           'methodName': LoggerUtil._findCaller()[2],
                                           'lineNo': LoggerUtil._findCaller()[1]})
    
    @staticmethod
    def warn(msg):
        LoggerUtil.ins.logger.setLevel(logging.WARN)
        LoggerUtil.ins.logger.warn(Fore.RED + 'WARN : \n' + msg,
                                   extra={'fileName': LoggerUtil._findCaller()[0],
                                          'methodName': LoggerUtil._findCaller()[2],
                                          'lineNo': LoggerUtil._findCaller()[1]})
    
    @staticmethod
    def close_logger():
        # 移除handle
        if LoggerUtil.read_config("log_type") == '1':
            LoggerUtil.ins.logger.removeFilter(LoggerUtil.ins.file_handle)
        elif LoggerUtil.read_config("log_type") == '2':
            LoggerUtil.ins.logger.removeHandler(LoggerUtil.ins.consle_handler)
        elif LoggerUtil.read_config("log_type") == '3':
            LoggerUtil.ins.logger.removeHandler(LoggerUtil.ins.consle_handler)
            LoggerUtil.ins.logger.removeFilter(LoggerUtil.ins.file_handle)
    
    @staticmethod
    def is_exists(path):
        """
        判断文件夹是否存在
        :param path:文件夹路径
        :return: True 或者False
        """
        is_exist = os.path.exists(path)
        return is_exist
    
    @staticmethod
    def clear_data(path, duration=0):
        """
        清除一些过期数据
        :param path: 清除的文件夹路径
        :param duration: 清除的时间间隔 单位小时
        """
        time_now = time.time()
        for root, dirs, files in os.walk(path):
            for name in files:
                modify_time = os.stat(os.path.join(root, name)).st_ctime
                if time_now - modify_time > 60 * 60 * duration:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        print("删除文件异常", e)
            
            for dirname in dirs:
                modify_time = os.path.getctime(os.path.join(root, dirname))
                if (time_now - modify_time) > 60 * 60 * duration:
                    try:
                        shutil.rmtree(os.path.join(root, dirname))
                    except Exception as e:
                        print("删除文件夹异常", e)
    
    @staticmethod
    def mik_file(file_name):
        """
        创建文件
        :param file_name: 文件名称
        :return: 文件名称及路径
        """
        is_exist = LoggerUtil.is_exists(file_name)
        if not is_exist:
            try:
                file = open(file_name, "a+")
            except Exception as e:
                print("io异常:", e.args)
            return file.name
    
    @staticmethod
    def mik_dirs(path):
        """
        创建多层文件夹
        :param path:文件夹路径
        :return:
        """
        is_exist = LoggerUtil.is_exists(path)
        if not is_exist:
            os.makedirs(path)
    
    @staticmethod
    def read_config(key, section="LOGTYPE"):
        conf = ConfigParser(LoggerUtil.ini_path)
        return conf.get(section, key)
    
    @staticmethod
    def _currentframe():
        """
        获取当前执行的py文件名称(源码直接复制的)
        """
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back
    
    @staticmethod
    def _findCaller():
        """
        获取调用者所在的py文件.
        """
        project_name = os.getcwd().split('\\')[-2:][0]
        f = LoggerUtil._currentframe()
        if f is not None:
            # 对源码进行修改,多加了一个.f_back
            f = f.f_back.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            # log的打印方式为工程的绝对路径名称
            # rv = (co.co_filename, f.f_lineno, co.co_name)

            # 对下面方法进行的优化
            index = co.co_filename.find("UI_Selenium_OpenCV_Ji")
            if index != -1:
                pro_names = co.co_filename[index:]
                # 路径中存在左斜杠或者右斜杠,所以均进行替换
                pro_names = pro_names.replace('/', ' - ')
                pro_names = pro_names.replace('\\', ' - ')
            
            # pro_list = co.co_filename.split('/')
            # pro_names_list = []
            # for i in range(0, len(pro_list)):
            #     if pro_list[i] == project_name:
            #         pro_names_list = pro_list[i:]
            # pro_names = ' - '.join(pro_names_list)
            
            # log的打印方式为仅使用工程名字的方式
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv


if __name__ == '__main__':
    ll = LoggerUtil()
    ll.debug("hahhahaha嗯")
    # ll.info("奶奶腿滴")
    # ll.error("哎呀妈呀")
    ll.close_logger()
