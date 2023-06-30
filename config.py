import configparser
import datetime

def create_default_config(file_path):
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

def load_config(file_path):
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
    event_Time = "[" + time_str + "]"
    config = configparser.ConfigParser()
    try:
        with open(file_path) as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        print(event_Time + f"[信息][系统][配置文件] 无法检测到配置文件,已创建默认配置文件")
        create_default_config(file_path)
        with open(file_path) as config_file:
            config.read_file(config_file)
    except configparser.MissingSectionHeaderError as e:
        print(event_Time + f"[错误][系统][配置文件] 配置文件加载失败：{str(e)}")
        return None

    return config

def get_config(section, option):
    config = load_config('config.ini')
    if config is not None:
        try:
            value = config.get(section, option)
            return value
        except configparser.Error as e:
            print(f"配置文件解析错误：{str(e)}")
    return None
