import os
import sys
import inspect
import traceback
from importlib import reload
from utils.Manager.Log_Manager import Log
from utils.Manager.Config_Manager import config_create, config_load
from Global.Global import GlobalVal

class PluginManage:
    def __init__(self, plugin_path="plugins"):
        """
        初始化插件管理器

        Args:
            plugin_path (str): 插件目录路径
        """
        self.plugin_path = plugin_path
        self.logger = Log()
        config_create()
        self.config = config_load()


    def check_plugin_directory(self):
        """检查插件目录是否存在，如果不存在则创建"""
        self.logger.info(message="正在检查插件目录 ...", flag="PluginManage")
        if not os.path.isdir(self.plugin_path):
            self.logger.warning(message=f"未找到插件目录 {self.plugin_path}，正在创建", flag="PluginManage")
            os.mkdir(self.plugin_path)

    def load_plugins(self):
        """
        加载所有插件目录中的插件，并返回插件对象列表

        Returns:
            list: 加载的插件对象列表
        """
        self.check_plugin_directory()
        self.logger.info(message="正在获取插件列表...", flag="PluginManage")

        plugin_list = [f for f in os.listdir(self.plugin_path) if f.endswith(('.py', '.pyc'))]

        if self.config["main"]["Debug"] == "true":
            self.logger.debug(message="插件列表：" + str(plugin_list), flag="PluginManage")

        self.logger.info(message="正在加载插件", flag="PluginManage")
        for plugin in plugin_list:
            self.load_single_plugin(plugin)

        self.logger.info(message=f"已成功加载 {len(GlobalVal.loaded_plugins)} 个插件", flag="PluginManage")
        return GlobalVal.loaded_plugins

    def load_single_plugin(self, plugin_filename):
        """
        加载单个插件文件
        """
        module_name, _ = os.path.splitext(plugin_filename)
        try:
            if f"{self.plugin_path}.{module_name}" in sys.modules:
                self.logger.warning(message=f"插件 {module_name} 已加载，跳过重复加载", flag="PluginManage")
                return

            module = __import__(f"{self.plugin_path}.{module_name}", fromlist=[module_name])
            plugin_class = getattr(module, "Plugin", None)

            if inspect.isclass(plugin_class):
                plugin_instance = plugin_class()
                GlobalVal.loaded_plugins.append((module_name, plugin_instance))
                self.display_plugin_info(module_name, plugin_instance)
            else:
                self.logger.warning(message=f"加载插件 {module_name} 失败，插件缺少主要类 'Plugin'", flag="PluginManage")
        except Exception:
            traceback_str = traceback.format_exc()
            self.logger.error(message=f"加载插件 {module_name} 失败，错误详情：\n{traceback_str}", flag="PluginManage")

    def display_plugin_info(self, module_name, plugin_instance):
        """
        显示插件信息
        """
        try:
            plugin_info = getattr(plugin_instance, 'get_plugin_info', lambda: {})
            plugin_name = plugin_info().get('name', module_name)
            plugin_display_name = f"{plugin_name} ({module_name})" if plugin_name != module_name else module_name
        except Exception as info_error:
            self.logger.warning(message=f"插件 {module_name} 信息加载失败：{info_error}", flag="PluginManage")
            plugin_display_name = module_name

        self.logger.info(message=f"成功加载插件 {plugin_display_name}", flag="PluginManage")

    def reload_plugin(self, module_name):
        """
        重新加载指定插件

        Returns:
            str: 重新加载结果信息
        """
        try:
            full_module_name = f"{self.plugin_path}.{module_name}"
            if full_module_name in sys.modules:
                module = sys.modules[full_module_name]
                reload(module)
                message = f"插件 {module_name} 已重新加载"
                self.logger.info(message=message, flag="PluginManage")
                return message
            else:
                message = f"插件 {module_name} 未加载，无法重新加载"
                self.logger.warning(message=message, flag="PluginManage")
                return message
        except Exception:
            traceback_str = traceback.format_exc()
            message = f"重新加载插件 {module_name} 失败，错误详情：\n{traceback_str}"
            self.logger.error(message=message, flag="PluginManage")
            return message

    def reload_all_plugins(self):
        """
        重新加载所有插件

        Returns:
            list: 每个插件重新加载的结果信息
        """
        self.logger.info(message="正在重新加载所有插件...", flag="PluginManage")
        results = [self.reload_plugin(module_name) for module_name, _ in GlobalVal.loaded_plugins]
        self.logger.info(message="所有插件已重新加载完成", flag="PluginManage")
        return results

    def list_plugins(self):
        """
        显示已加载的插件列表

        Returns:
            list: 已加载插件的模块名列表
        """
        if not GlobalVal.loaded_plugins:
            message = "没有已加载的插件"
            self.logger.info(message=message, flag="PluginManage")
            return []

        self.logger.info(message="已加载的插件列表：", flag="PluginManage")
        plugin_names = [module_name for module_name, _ in GlobalVal.loaded_plugins]
        for name in plugin_names:
            self.logger.info(message=f"- {name}", flag="PluginManage")
        return plugin_names
