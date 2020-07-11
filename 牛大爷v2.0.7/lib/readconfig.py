import configparser
import os

#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser() #实例化类
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.ini'   #获取文件根目录
    config.read(path,encoding='utf-8')   #读取路径上的配置文件，并读取方式utf8文字格式
    return config.get(section, key)

#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录