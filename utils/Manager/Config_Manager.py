import json
import os
from utils.Manager.Log_Manager import Log

logger = Log()

DEFAULT_CONFIG = {
    "main": {
        "Debug": "False",
        "master_qq": "123456"
    }
}

def config_create():
    """
    创建默认主配置文件。
    如果配置文件已存在，则不会覆盖。

    Returns:
        None
    """
    config_path = "config/Bot/config.json"
    folder_path = "config/Bot"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(config_path):
        logger.info(message="未找到主配置文件。正在创建默认配置文件", flag="Config")
        try:
            with open(config_path, "w") as config_file:
                json.dump(DEFAULT_CONFIG, config_file, indent=4)
            logger.info(message="默认配置文件创建成功", flag="Config")
        except Exception as e:
            logger.error(message=f"创建配置文件失败: {e}", flag="Config")


def config_load():
    """
    加载主配置文件。

    Returns:
        dict: 配置文件的内容。如果文件不存在或读取失败，则返回 None。
    """
    config_path = "config/Bot/config.json"
    if not os.path.exists(config_path):
        logger.error(message="主配置文件不存在，请创建配置文件。", flag="Config")
        return None
    
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            return config
    except json.JSONDecodeError as e:
        logger.error(message=f"加载配置文件失败，JSON解析错误: {e}", flag="Config")
    except Exception as e:
        logger.error(message=f"加载配置文件失败: {e}", flag="Config")
    
    return None


def connect_config_load():
    """
    加载连接配置文件。

    Returns:
        dict: 配置文件的内容。如果文件不存在或读取失败，则返回 None。
    """
    config_path = "config/Bot/connect.json"
    if not os.path.exists(config_path):
        logger.error(message="连接配置文件不存在，请创建连接配置文件。", flag="Config")
        return None
    
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            return config
    except json.JSONDecodeError as e:
        logger.error(message=f"加载连接配置文件失败，JSON解析错误: {e}", flag="Config")
    except Exception as e:
        logger.error(message=f"加载连接配置文件失败: {e}", flag="Config")
    
    return None
