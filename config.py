import configparser
import datetime

def create_default_config(file_path: str):
    """
    创建默认配置文件。
    
    Args:
        file_path (str): 配置文件路径。
    """
    config = configparser.ConfigParser()
    config['main'] = {
        'master_qq': '123456'
    }
    config['gocq'] = {
        'host': '127.0.0.1',
        'ws_port': '114',
        'http_port': '123'
    }
    with open(file_path, 'w') as config_file:
        config.write(config_file)

def load_config(file_path: str) -> configparser.ConfigParser:
    """
    加载配置文件。
    
    Args:
        file_path (str): 配置文件路径。
    
    Returns:
        configparser.ConfigParser: 解析后的配置对象。
    """
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
    event_Time = "[" + time_str + "]"
    config = configparser.ConfigParser()
    
    try:
        with open(file_path) as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        print(event_Time + "[INFO][System][Config] 未找到配置文件。正在创建默认配置文件。")
        create_default_config(file_path)
        with open(file_path) as config_file:
            config.read_file(config_file)
    except configparser.MissingSectionHeaderError as e:
        print(event_Time + f"[ERROR][System][Config] 加载配置文件失败：{str(e)}")
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
    config = load_config('config.ini')
    
    if config is not None:
        try:
            value = config.get(section, option)
            return value
        except configparser.Error as e:
            print(f"配置文件解析错误：{str(e)}")
    
    return None
