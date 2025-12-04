# utils/Manager/Plugin_Manager.py
import os
import sys
import importlib
import inspect
import asyncio
import traceback
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import importlib.util

from utils.Manager.Log_Manager import Log
from utils.Manager.Config_Manager import config_load
from Global.Global import GlobalVal


class PluginStatus(Enum):
    """插件状态枚举"""
    LOADED = "已加载"
    UNLOADED = "已卸载"
    ERROR = "错误"
    LOADING = "加载中"
    UNLOADING = "卸载中"


class EventPriority(Enum):
    """事件优先级"""
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    priority: EventPriority = EventPriority.NORMAL


@dataclass
class LoadedPlugin:
    """已加载的插件"""
    module_name: str
    plugin_instance: Any
    info: PluginInfo
    status: PluginStatus
    registered_events: Set[str] = field(default_factory=set)
    
    
class EventRegistry:
    """事件注册表"""
    
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}
        self._plugin_events: Dict[str, Set[str]] = {}  # 插件名 -> 事件集合
        
    def register(self, event_name: str, handler: Callable, plugin_name: str) -> bool:
        """注册事件处理器"""
        if event_name not in self._events:
            self._events[event_name] = []
            
        self._events[event_name].append(handler)
        
        if plugin_name not in self._plugin_events:
            self._plugin_events[plugin_name] = set()
        self._plugin_events[plugin_name].add(event_name)
        
        return True
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """注销插件的所有事件"""
        if plugin_name in self._plugin_events:
            for event_name in self._plugin_events[plugin_name]:
                if event_name in self._events:
                    # 移除该插件的所有处理器
                    self._events[event_name] = [
                        h for h in self._events[event_name]
                        if not (hasattr(h, '__self__') and 
                               hasattr(h.__self__, '__class__') and
                               h.__self__.__class__.__name__ == plugin_name)
                    ]
            del self._plugin_events[plugin_name]
    
    def get_handlers(self, event_name: str) -> List[Callable]:
        """获取事件处理器列表"""
        return self._events.get(event_name, [])


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugin_path: str = "plugins"):
        self.plugin_path = Path(plugin_path)
        self.logger = Log()
        self.config = None
        self._plugins: Dict[str, LoadedPlugin] = {}
        self._event_registry = EventRegistry()
        self._loading_lock = asyncio.Lock()
        
    async def initialize(self) -> None:
        """初始化插件管理器"""
        self.config = config_load()
        await self._ensure_plugin_directory()
        
    async def _ensure_plugin_directory(self) -> None:
        """确保插件目录存在"""
        if not self.plugin_path.exists():
            self.logger.warning(f"插件目录 {self.plugin_path} 不存在，正在创建", flag="PluginManager")
            self.plugin_path.mkdir(parents=True, exist_ok=True)
            
    def _get_plugin_files(self) -> List[Path]:
        """获取插件文件列表"""
        return [
            f for f in self.plugin_path.iterdir()
            if f.is_file() and f.suffix == '.py' and not f.name.startswith('_')
        ]
    
    async def load_all_plugins(self) -> int:
        """加载所有插件"""
        self.logger.info("开始加载插件...", flag="PluginManager")
        
        plugin_files = self._get_plugin_files()
        loaded_count = 0
        
        for plugin_file in plugin_files:
            if await self.load_plugin(plugin_file.stem):
                loaded_count += 1
                
        # 更新全局插件列表
        self._update_global_plugin_list()
        
        self.logger.info(f"插件加载完成，共加载 {loaded_count}/{len(plugin_files)} 个插件", 
                        flag="PluginManager")
        return loaded_count
    
    async def load_plugin(self, plugin_name: str) -> bool:
        """加载单个插件"""
        async with self._loading_lock:
            if plugin_name in self._plugins:
                self.logger.warning(f"插件 {plugin_name} 已加载", flag="PluginManager")
                return False
                
            try:
                # 构建插件文件的完整路径
                plugin_file = self.plugin_path / f"{plugin_name}.py"
                if not plugin_file.exists():
                    self.logger.error(f"插件文件不存在: {plugin_file}", flag="PluginManager")
                    return False
            
                # 动态添加插件目录到 sys.path
                plugin_dir_str = str(self.plugin_path.absolute())
                if plugin_dir_str not in sys.path:
                    sys.path.insert(0, plugin_dir_str)
            
                # 使用 spec 加载模块
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                if spec is None or spec.loader is None:
                    self.logger.error(f"无法创建模块 spec: {plugin_name}", flag="PluginManager")
                    return False
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module  # 注册到 sys.modules
                spec.loader.exec_module(module)
                
                # 查找Plugin类
                plugin_class = getattr(module, "Plugin", None)
                if not plugin_class or not inspect.isclass(plugin_class):
                    self.logger.error(f"插件 {plugin_name} 缺少 Plugin 类", flag="PluginManager")
                    return False
                
                # 创建插件实例
                plugin_instance = plugin_class()
                
                # 获取插件信息
                plugin_info = self._get_plugin_info(plugin_instance, plugin_name)
                
                # 创建LoadedPlugin对象
                loaded_plugin = LoadedPlugin(
                    module_name=plugin_name,
                    plugin_instance=plugin_instance,
                    info=plugin_info,
                    status=PluginStatus.LOADED
                )
                
                # 注册插件事件
                await self._register_plugin_events(plugin_instance, plugin_name)
                
                # 保存插件
                self._plugins[plugin_name] = loaded_plugin
                
                # 调用插件的初始化方法
                if hasattr(plugin_instance, 'on_load'):
                    await self._safe_call(plugin_instance.on_load)
                
                self.logger.info(f"成功加载插件: {plugin_info.name} v{plugin_info.version}", 
                               flag="PluginManager")
                return True
                
            except Exception as e:
                self.logger.error(f"加载插件 {plugin_name} 失败: {traceback.format_exc()}", 
                                flag="PluginManager")
                return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        async with self._loading_lock:
            if plugin_name not in self._plugins:
                self.logger.warning(f"插件 {plugin_name} 未加载", flag="PluginManager")
                return False
            
            try:
                plugin = self._plugins[plugin_name]
                plugin.status = PluginStatus.UNLOADING
                
                # 调用插件的卸载方法
                if hasattr(plugin.plugin_instance, 'on_unload'):
                    await self._safe_call(plugin.plugin_instance.on_unload)
                
                # 注销事件
                self._event_registry.unregister_plugin(plugin_name)
                
                # 从系统中移除模块
                module_path = f"{self.plugin_path.name}.{plugin_name}"
                if module_path in sys.modules:
                    del sys.modules[module_path]
                
                # 删除插件记录
                del self._plugins[plugin_name]
                
                # 更新全局列表
                self._update_global_plugin_list()
                
                self.logger.info(f"成功卸载插件: {plugin.info.name}", flag="PluginManager")
                return True
                
            except Exception as e:
                self.logger.error(f"卸载插件 {plugin_name} 失败: {traceback.format_exc()}", 
                                flag="PluginManager")
                return False
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """重新加载插件"""
        self.logger.info(f"正在重新加载插件: {plugin_name}", flag="PluginManager")
        
        # 先卸载
        if plugin_name in self._plugins:
            if not await self.unload_plugin(plugin_name):
                return False
        
        # 再加载
        return await self.load_plugin(plugin_name)
    
    async def unload_all_plugins(self) -> None:
        """卸载所有插件"""
        plugin_names = list(self._plugins.keys())
        for plugin_name in plugin_names:
            await self.unload_plugin(plugin_name)
    
    def get_plugin_list(self) -> List[Dict[str, Any]]:
        """获取插件列表"""
        return [
            {
                "name": plugin.info.name,
                "module": plugin.module_name,
                "version": plugin.info.version,
                "status": plugin.status.value,
                "author": plugin.info.author,
                "description": plugin.info.description
            }
            for plugin in self._plugins.values()
        ]
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """获取单个插件信息"""
        if plugin_name in self._plugins:
            plugin = self._plugins[plugin_name]
            return {
                "name": plugin.info.name,
                "module": plugin.module_name,
                "version": plugin.info.version,
                "status": plugin.status.value,
                "author": plugin.info.author,
                "description": plugin.info.description,
                "dependencies": plugin.info.dependencies,
                "registered_events": list(plugin.registered_events)
            }
        return None
    
    async def trigger_event(self, event_name: str, *args, **kwargs) -> None:
        """触发事件"""
        # self.logger.info(f"触发事件: {event_name}, 已加载插件: {list(self._plugins.keys())}", 
        #             flag="PluginManager")
        tasks = []
        
        # 从插件实例中触发事件
        for plugin_name, plugin in self._plugins.items():
            if hasattr(plugin.plugin_instance, event_name):
                # self.logger.info(f"插件 {plugin_name} 响应事件 {event_name}", 
                #                flag="PluginManager")
                method = getattr(plugin.plugin_instance, event_name)
                if callable(method):
                    task = asyncio.create_task(
                        self._safe_call(method, *args, **kwargs)
                    )
                    tasks.append(task)
            else:
                pass
                # self.logger.debug(f"插件 {plugin_name} 没有 {event_name} 方法", 
                #                 flag="PluginManager")
        
        # 从注册表中触发事件
        handlers = self._event_registry.get_handlers(event_name)
        for handler in handlers:
            task = asyncio.create_task(
                self._safe_call(handler, *args, **kwargs)
            )
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _register_plugin_events(self, plugin_instance: Any, plugin_name: str) -> None:
        """注册插件事件处理器"""
        # 获取所有公开方法
        for attr_name in dir(plugin_instance):
            if not attr_name.startswith('_'):
                attr = getattr(plugin_instance, attr_name)
                if callable(attr):
                    # 检查是否有事件装饰器标记
                    if hasattr(attr, '_event_handler'):
                        event_name = getattr(attr, '_event_name', attr_name)
                        self._event_registry.register(event_name, attr, plugin_name)
                        
                        if plugin_name in self._plugins:
                            self._plugins[plugin_name].registered_events.add(event_name)
    
    def _get_plugin_info(self, plugin_instance: Any, plugin_name: str) -> PluginInfo:
        """获取插件信息"""
        if hasattr(plugin_instance, 'get_plugin_info'):
            info_dict = plugin_instance.get_plugin_info()
            return PluginInfo(
                name=info_dict.get('name', plugin_name),
                version=info_dict.get('version', '1.0.0'),
                author=info_dict.get('author', 'Unknown'),
                description=info_dict.get('description', ''),
                dependencies=info_dict.get('dependencies', [])
            )
        return PluginInfo(name=plugin_name)
    
    async def _safe_call(self, method: Callable, *args, **kwargs) -> Any:
        """安全调用方法"""
        try:
            if asyncio.iscoroutinefunction(method):
                return await method(*args, **kwargs)
            else:
                return method(*args, **kwargs)
        except Exception as e:
            method_name = getattr(method, '__name__', str(method))
            self.logger.error(f"调用方法 {method_name} 时出错: {traceback.format_exc()}", 
                            flag="PluginManager")
            return None
    
    def _update_global_plugin_list(self) -> None:
        """更新全局插件列表"""
        GlobalVal.plugin_list = [
            (plugin.module_name, plugin.plugin_instance)
            for plugin in self._plugins.values()
            if plugin.status == PluginStatus.LOADED
        ]
        GlobalVal.loaded_plugins = GlobalVal.plugin_list.copy()


# 事件装饰器
def event_handler(event_name: Optional[str] = None):
    """
    事件处理器装饰器
    
    使用方式:
    @event_handler("GroupMessage")
    async def on_group_message(self, api, message):
        pass
    """
    def decorator(func):
        func._event_handler = True
        func._event_name = event_name or func.__name__
        return func
    return decorator