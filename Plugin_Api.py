import datetime
import importlib
import os


def load_plugins():
    """
    加载插件目录中的插件文件并创建插件对象

    Returns:
        list: 插件对象列表
    """
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
    event_Time = "[" + time_str + "]"
    plugins = []
    plugin_dir = "plugins"  # 插件目录路径
    print(event_Time + f"[信息][系统] 正在加载插件")

    # 遍历插件目录中的文件
    for plugin_file in os.listdir(plugin_dir):
        if plugin_file.endswith(".py"):
            plugin_path = os.path.join(plugin_dir, plugin_file)
            module_name = os.path.splitext(plugin_file)[0]
            try:
                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "Plugin") and callable(getattr(module, "Plugin")):
                    plugins.append((module_name, getattr(module, "Plugin")()))
                    print(event_Time + f"[信息][插件][加载][{module_name}] 插件已加载")
                else:
                    print(event_Time + f"[警告][插件][跳过][{module_name}] Error: 插件缺少主要类'Plugin',跳过加载")
            except Exception as e:
                print(event_Time + f"[错误][插件][加载][{module_name}] Error: {str(e)}")
    print(event_Time + f"[信息][插件][系统] 全部插件已加载完毕")
    print(event_Time + f"[信息][系统] 正在等待Go-CQHTTP协议握手")

    return plugins


async def Plugins_Group_Message(message, plugins):
    """
    处理群消息的逻辑

    Args:
        message (str): 接收到的消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "GroupMessage") and callable(getattr(plugin, "GroupMessage")):
            try:
                await plugin.GroupMessage(message)
            except Exception as e:
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                event_Time = "[" + time_str + "]"
                print(event_Time + f"[错误][插件][执行][消息][{plugin_name}] Error: {str(e)}")
        else:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            event_Time = "[" + time_str + "]"
            #print(event_Time + f"[警告][插件][跳过][消息][{plugin_name}] 插件缺少 'GroupMessage' 方法，跳过执行。")


async def Plugins_Request(message, plugins):
    """
    处理请求事件的逻辑

    Args:
        message (str): 请求消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Request") and callable(getattr(plugin, "Request")):
            try:
                await plugin.Request(message)
            except Exception as e:
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                event_Time = "[" + time_str + "]"
                print(event_Time + f"[错误][插件][执行][事件][请求][{plugin_name}] Error: {str(e)}")
        else:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            event_Time = "[" + time_str + "]"
            #print(event_Time + f"[警告][插件][跳过][事件][请求][{plugin_name}] 插件缺少 'Request' 方法，跳过执行。")


async def Plugins_Notice_join(message, plugins):
    """
    处理进群事件的逻辑

    Args:
        message (str): 进群消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Notice_join") and callable(getattr(plugin, "Notice_join")):
            try:
                await plugin.Notice_join(message)
            except Exception as e:
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                event_Time = "[" + time_str + "]"
                print(event_Time + f"[错误][插件][执行][事件][进群][{plugin_name}] Error: {str(e)}")
        else:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            event_Time = "[" + time_str + "]"
            #print(event_Time + f"[警告][插件][跳过][事件][进群][{plugin_name}] 插件缺少 'Notice_join' 方法，跳过执行。")


async def Plugins_Notice_leave(message, plugins):
    """
    处理退群事件的逻辑

    Args:
        message (str): 退群消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Notice_leave") and callable(getattr(plugin, "Notice_leave")):
            try:
                await plugin.Notice_leave(message)
            except Exception as e:
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                event_Time = "[" + time_str + "]"
                print(event_Time + f"[错误][插件][执行][事件][退群][{plugin_name}] Error: {str(e)}")
        else:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            event_Time = "[" + time_str + "]"
            #print(event_Time + f"[警告][插件][跳过][事件][退群][{plugin_name}] 插件缺少 'Notice_leave' 方法，跳过执行。")
