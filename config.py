import configparser
import os

from LogSys import Log

logger = Log()


def create_default_config(file_path = "config/main.ini"):
    """
    创建默认配置文件。
    
    Args:
        file_path (str): 配置文件路径。
    """
    if not os.path.isfile(file_path):
        # Configuration file does not exist, create a default configuration file
        folder = os.path.exists("config")
        if not folder:
            os.makedirs("config")
    config = configparser.ConfigParser()
    config['main'] = {
        'Debug': False,
        'master_qq': '123456'
    }
    config['gocq'] = {
        'host': '127.0.0.1',
        'ws_port': '114',
        'http_port': '123'
    }
    with open(file_path, 'w') as config_file:
        config.write(config_file)


def load_config(file_path = "config/main.ini") -> None:
    """
    加载配置文件。
    
    Args:
        file_path (str): 配置文件路径。
    
    Returns:
        configparser.ConfigParser: 解析后的配置对象。
    """
    config = configparser.ConfigParser()

    try:
        with open(file_path) as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        logger.info(message="未找到主配置文件。正在创建默认配置文件", flag="Config")
        create_default_config(file_path)
        with open(file_path) as config_file:
            config.read_file(config_file)
    except configparser.MissingSectionHeaderError as e:
        logger.error(message="无法载入主配置文件,Error: " + str(e), flag="Config")
        return None

    return config


def get_config(section: str, option: str) -> str:
    """
    获取配置文件中指定部分和选项的值。
    
    Args:
        section (str): 配置文件部分名称。
        option (str): 配置文件选项名称。
    
    Returns:
        str: 配置文件中指定选项的值。
    """
    config = load_config()

    if config is not None:
        try:
            value = config.get(section, option)
            return value
        except configparser.Error as e:
            logger.error(message="主配置文件解析错误,Error: " + str(e), flag="Config")
