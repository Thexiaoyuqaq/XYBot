from utils.Manager.Log_Manager import Log
import inspect
import os
from config import *

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
    loadedPlugins = []
    plugin_path = 'plugins'

    logger.info(message="正在检查插件目录 ...", flag=FILE_NAME)
    if not os.path.isdir(plugin_path):
        logger.warning(message=f"未找到插件目录 {plugin_path}，正在创建", flag=FILE_NAME)
        os.mkdir(plugin_path)

    logger.info(message="正在获取插件列表...", flag=FILE_NAME)
    pluginList = os.listdir("plugins")

    if config["main"]["Debug"] == "true":
        logger.debug(message="插件列表：" + str(pluginList), flag=FILE_NAME)

    for plugin in pluginList:
        if plugin.endswith(".py"):
            module_name = plugin[:-3]
            try:
                module = getattr(__import__(f"plugins.{module_name}"), module_name)
                if inspect.isclass(getattr(module, "Plugin", False)):
                    # 获取插件信息和前置库依赖
                    plugin_instance = getattr(module, "Plugin")()
                    try:
                        plugin_info = plugin_instance.get_plugin_info()
                    except Exception as e:
                        plugin_info = {'name': f'{module_name}','author': '未知','version': '1.0.0',}
                    loadedPlugins.append((module_name, getattr(module, "Plugin")()))
                    logger.info(message=f"加载插件 {plugin_info['name']}   V{plugin_info['version']}     作者:{plugin_info['author']}", flag=FILE_NAME)#{module_name}
                else:
                    logger.warning(message=f"加载插件 {module_name} 失败，插件缺少主要类 'Plugin'", flag=FILE_NAME)
            except Exception as e:
                logger.error(message=f"无法加载 {module_name}，加载发生错误：{e}", flag=FILE_NAME)

    logger.info(message=f"已成功加载 {len(loadedPlugins)} 个插件", flag=FILE_NAME)
    return loadedPlugins
