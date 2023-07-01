# -*- coding:utf-8 -*-
# @FileName :Plugin_Manager.py
# @Time     : 3:48
# @Author   :Endermite

# 重构Plugin_Api.py

import os
from LogSys import Log
import inspect
from config import get_config

FILE_NAME = "Plugin_Manager"
logger = Log()


def load_plugins():
    loadedPlugins = []
    plugin_path = 'plugins'
    logger.info(message="正在检查插件目录 ...", flag=FILE_NAME)
    if not os.path.isdir(plugin_path):
        logger.warning(message=f"未找到插件目录{plugin_path} ，正在创建", flag=FILE_NAME)
        os.mkdir(plugin_path)
    logger.info(message="正在获取插件列表...", flag=FILE_NAME)
    pluginList = os.listdir("plugins")
    #pluginList.pop(pluginList.index("__pycache__"))
    if get_config('main', 'Debug') == True :
        logger.debug(message="插件列表：" + str(pluginList), flag=FILE_NAME)

    logger.info(message="正在加载插件", flag=FILE_NAME)
    for plugin in pluginList:
        if plugin.endswith(".py"):
            module_name = plugin[:-3]
            try:
                module = getattr(__import__(f"plugins.{module_name}"), module_name)
                if inspect.isclass(getattr(module, "Plugin", False)):
                    loadedPlugins.append((module_name, getattr(module, "Plugin")()))
                    logger.info(message=f"成功加载插件 {module_name}", flag=FILE_NAME)
                else:
                    logger.warning(message=f"加载插件 {module_name} 失败，插件缺少主要类'Plugin'", flag=FILE_NAME)
            except Exception as e:
                logger.error(message=f"加载插件 {module_name} 失败，加载发生错误：{e}", flag=FILE_NAME)
    logger.info(message=f"已成功加载 {loadedPlugins.__len__()} 个插件", flag=FILE_NAME)
    return loadedPlugins
