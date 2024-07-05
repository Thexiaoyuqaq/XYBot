# -*- coding:utf-8 -*-
# @FileName :Plugin_Manager.py
# @Time     : 3:48
# @Author   :Endermite

import os
import inspect
import traceback
from utils.Manager.Log_Manager import Log
from utils.Manager.Config_Manager import config_create, config_load

FILE_NAME = "Plugin_Manager"
logger = Log()
config_create()
config = config_load()

def load_plugins():
    """
    加载插件目录中所有插件，并返回插件对象列表

    Returns:
        list: 加载的插件对象列表
    """
    loaded_plugins = []
    plugin_path = "plugins"

    logger.info(message="正在检查插件目录 ...", flag=FILE_NAME)
    if not os.path.isdir(plugin_path):
        logger.warning(message=f"未找到插件目录 {plugin_path}，正在创建", flag=FILE_NAME)
        os.mkdir(plugin_path)

    logger.info(message="正在获取插件列表...", flag=FILE_NAME)
    plugin_list = os.listdir(plugin_path)

    if config["main"]["Debug"] == "true":
        logger.debug(message="插件列表：" + str(plugin_list), flag=FILE_NAME)

    logger.info(message="正在加载插件", flag=FILE_NAME)
    for plugin in plugin_list:
        if plugin.endswith(".py") or plugin.endswith(".pyc"):
            module_name = plugin[:-3]
            try:
                module = getattr(__import__(f"plugins.{module_name}"), module_name)
                plugin_class = getattr(module, "Plugin", None)
                if inspect.isclass(plugin_class):
                    plugin_instance = plugin_class()
                    loaded_plugins.append((module_name, plugin_instance))
                    plugin_info = getattr(plugin_instance, 'get_plugin_info', None)
                    if plugin_info:
                        plugin_name = plugin_info().get('name', module_name)
                        plugin_display_name = f"{plugin_name} ({module_name})" if plugin_name != module_name else module_name
                    else:
                        plugin_display_name = module_name
                    logger.info(message=f"成功加载插件 {plugin_display_name}", flag=FILE_NAME)
                else:
                    logger.warning(message=f"加载插件 {module_name} 失败，插件缺少主要类 'Plugin'", flag=FILE_NAME)
            except Exception as e:
                traceback_str = traceback.format_exc()
                logger.error(message=f"加载插件 {module_name} 失败，加载发生错误：{str(traceback_str)}", flag=FILE_NAME)

    logger.info(message=f"已成功加载 {len(loaded_plugins)} 个插件", flag=FILE_NAME)
    return loaded_plugins
