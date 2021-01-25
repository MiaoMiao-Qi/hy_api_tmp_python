import configparser
import os


class Config(object):
    """
    读取配置文件函数
    """
    def __init__(self, file_name):
        self.config = configparser.RawConfigParser() # configparser.ConfigParser()
        path = os.path.split(os.path.realpath(__file__))[0] + '/%s.conf' % file_name
        self.config.read(path, encoding='UTF-8')
        
    def getConfig(self, key, section=None):
        if section:
            return self.config.get(section, key)
        else:
            return self.config.get('general', key)


if __name__ == "__main__":
    cfg = Config('config/config_dongfeng')
    print(cfg.getConfig('mail_server', 'general'))


  


