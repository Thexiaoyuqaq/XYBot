import json
import os

from utils.Manager.Log_Manager import Log

logger = Log()

def config_create():
    """
    创建默认主配置文件。
    """    
    config_path = f"config/Bot/config.ini"
    folder_path = f"config/Bot"

    folder = os.path.exists(folder_path)

    if not folder: 
        os.makedirs(folder_path)
    if not os.path.exists(config_path):
        logger.info(message="未找到主配置文件。正在创建默认配置文件", flag="Config")
        with open(config_path, "w") as config_file:
            config = {
                "main": {
                    "Debug": "False",
                    "master_qq": "123456"
                }
            }
            json.dump(config, config_file)

def config_load():
    """
    加载主配置文件。
    
    Returns:
        str: 配置文件的内容
    """
    config_path = f"config/Bot/config.ini"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
        return config
def connect_config_load():
    """
    加载主配置文件。
    
    Returns:
        str: 配置文件的内容
    """
    config_path = f"config/Bot/connect.ini"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
        return config