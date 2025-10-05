# utils/Api/Plugin_Api.py
import asyncio
import traceback
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from utils.Manager.Log_Manager import Log
from utils.Manager.Plugin_Manager import PluginManager
from Global.Global import GlobalVal


@dataclass
class MessageAPI:
    """消息API接口，提供给插件使用"""
    
    def __init__(self, event_type: str, message: Dict[str, Any]):
        self.event_type = event_type
        self.message = message
        self._cache = {}
    
    async def get(self, *keys: str, default: Any = None) -> Any:
        """通用获取方法"""
        data = self.message
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, {})
            else:
                return default
        return data if data != {} else default
    
    # 群组相关
    async def get_group_id(self) -> Optional[int]:
        """获取群组ID"""
        cache_key = "group_id"
        if cache_key not in self._cache:
            if self.event_type == "GroupMessage":
                self._cache[cache_key] = await self.get("group", "group_id")
            else:
                self._cache[cache_key] = await self.get("event", "group_id")
        return self._cache[cache_key]
    
    async def get_group_name(self) -> Optional[str]:
        """获取群组名称"""
        return await self.get("group", "group_name")
    
    async def get_group_member_count(self) -> Optional[int]:
        """获取群成员数量"""
        return await self.get("group", "group_member_count")
    
    # 发送者相关
    async def get_sender_id(self) -> Optional[int]:
        """获取发送者ID"""
        cache_key = "sender_id"
        if cache_key not in self._cache:
            if self.event_type in ["GroupMessage", "PrivateMessage"]:
                self._cache[cache_key] = await self.get("sender", "user_id")
            else:
                self._cache[cache_key] = await self.get("event", "user_id")
        return self._cache[cache_key]
    
    async def get_sender_nickname(self) -> Optional[str]:
        """获取发送者昵称"""
        return await self.get("sender", "user_nickname")
    
    async def get_sender_card(self) -> Optional[str]:
        """获取发送者群名片"""
        return await self.get("sender", "user_card")
    
    async def get_sender_role(self) -> Optional[str]:
        """获取发送者角色"""
        return await self.get("sender", "user_role")
    
    # 消息相关
    async def get_message_content(self) -> str:
        """获取消息内容"""
        return await self.get("message", "message") or ""
    
    async def get_message_id(self) -> Optional[int]:
        """获取消息ID"""
        return await self.get("message", "message_id")
    
    async def get_message_time(self) -> Optional[int]:
        """获取消息时间"""
        return await self.get("message", "message_time")
    
    async def get_raw_message(self) -> Dict[str, Any]:
        """获取原始消息数据"""
        return await self.get("message", "raw") or {}
    
    # 请求相关
    async def get_request_flag(self) -> Optional[str]:
        """获取请求标识"""
        return await self.get("flag")
    
    async def get_request_comment(self) -> Optional[str]:
        """获取请求备注"""
        return await self.get("comment")
    
    async def get_request_type(self) -> Optional[str]:
        """获取请求类型"""
        return await self.get("request", "sub_type")
    
    # 事件相关
    async def get_operator_id(self) -> Optional[int]:
        """获取操作者ID"""
        return await self.get("event", "operator_id")
    
    async def get_event_time(self) -> Optional[int]:
        """获取事件时间"""
        return await self.get("event", "time")
    
    async def get_event_sub_type(self) -> Optional[str]:
        """获取事件子类型"""
        return await self.get("event", "sub_type")
    
    # 兼容旧API
    async def Get_Group_GroupID(self) -> Optional[int]:
        """兼容旧API - 获取群组ID"""
        return await self.get_group_id()
    
    async def Get_Sender_UserID(self) -> Optional[int]:
        """兼容旧API - 获取发送者ID"""
        return await self.get_sender_id()
    
    async def Get_Message_ID(self) -> Optional[int]:
        '''兼容旧API - 获取消息ID'''
        return await self.get_message_id()
    
    async def Get_Message_Message(self) -> str:
        """兼容旧API - 获取消息内容"""
        return await self.get_message_content()
    async def Get_Message_Content(self) -> str:
        return await self.get_message_content()
    
    async def Get_Sender_NickName(self) -> str:
        """兼容旧API - 获取用户名"""
        return await self.get_sender_nickname()
    async def Get_Sender_UserRole(self) -> str:
        """兼容旧API - 获取用户头街"""
        return await self.get_sender_role()


    async def Get_Operator_UserID(self) -> Optional[int]:
        """兼容旧API - 获取操作者ID"""
        return await self.get_operator_id()

    async def Get_User_JoinType(self) -> Optional[str]:
        """兼容旧API - 获取用户加入类型"""
        return await self.get_event_sub_type()
        


class PluginAPI:
    """插件API管理器"""
    
    def __init__(self):
        self.logger = Log()
        self.plugin_manager: Optional[PluginManager] = None
        self._running_tasks: List[asyncio.Task] = []
    
    def set_plugin_manager(self, manager: PluginManager) -> None:
        """设置插件管理器"""
        self.plugin_manager = manager
    
    async def _execute_plugin_event(self, event_name: str, message: Dict[str, Any]) -> None:
        """执行插件事件"""
        if not self.plugin_manager:
            self.plugin_manager = PluginManager()
            await self.plugin_manager.initialize()

        # self.logger.info(f"开始执行插件事件: {event_name}", flag="PluginAPI")
        
        # 创建消息API
        message_api = MessageAPI(event_name, message)
        
        # 触发事件
        await self.plugin_manager.trigger_event(event_name, message_api, message)

        # self.logger.info(f"插件事件 {event_name} 执行完成", flag="PluginAPI")
    
    async def _safe_execute(self, event_name: str, message: Dict[str, Any]) -> None:
        """安全执行事件"""
        try:
            task = asyncio.create_task(self._execute_plugin_event(event_name, message))
            self._running_tasks.append(task)
            
            # 清理已完成的任务
            self._running_tasks = [t for t in self._running_tasks if not t.done()]
            
        except Exception as e:
            self.logger.error(f"执行插件事件 {event_name} 时出错: {traceback.format_exc()}", 
                            flag="PluginAPI")
    
    # 消息事件
    async def Plugins_Group_Message(self, message: Dict[str, Any]) -> None:
        """处理群消息事件"""
        await self._safe_execute("GroupMessage", message)
    
    async def Plugins_Private_Message(self, message: Dict[str, Any]) -> None:
        """处理私聊消息事件"""
        await self._safe_execute("PrivateMessage", message)
    
    # 请求事件
    async def Plugins_Request_Friend(self, message: Dict[str, Any]) -> None:
        """处理好友请求事件"""
        await self._safe_execute("Request_Friend", message)
    
    async def Plugins_Request_Group(self, message: Dict[str, Any]) -> None:
        """处理群请求事件"""
        await self._safe_execute("Request_Group", message)
    
    # 通知事件
    async def Plugins_Notice_GroupIncrease(self, message: Dict[str, Any]) -> None:
        """处理群成员增加事件"""
        await self._safe_execute("Notice_GroupIncrease", message)
    
    async def Plugins_Notice_GroupDecrease(self, message: Dict[str, Any]) -> None:
        """处理群成员减少事件"""
        await self._safe_execute("Notice_GroupDecrease", message)
    
    # 生命周期事件
    async def Plugins_Start(self) -> None:
        """插件启动事件"""
        self.logger.info("触发插件启动事件", flag="PluginAPI")
        if self.plugin_manager:
            await self.plugin_manager.trigger_event("Start")
    
    async def Plugins_Stop(self) -> None:
        """插件停止事件"""
        self.logger.info("触发插件停止事件", flag="PluginAPI")
        
        # 取消所有运行中的任务
        for task in self._running_tasks:
            if not task.done():
                task.cancel()
        
        # 等待任务完成
        if self._running_tasks:
            await asyncio.gather(*self._running_tasks, return_exceptions=True)
        
        self._running_tasks.clear()
        
        if self.plugin_manager:
            await self.plugin_manager.trigger_event("Stop")
    
    # 插件管理API
    async def load_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """加载插件"""
        if not self.plugin_manager:
            return {"success": False, "message": "插件管理器未初始化"}
        
        try:
            success = await self.plugin_manager.load_plugin(plugin_name)
            if success:
                return {"success": True, "message": f"插件 {plugin_name} 加载成功"}
            else:
                return {"success": False, "message": f"插件 {plugin_name} 加载失败"}
        except Exception as e:
            self.logger.error(f"加载插件 {plugin_name} 时出错: {str(e)}", flag="PluginAPI")
            return {"success": False, "message": str(e)}
    
    async def unload_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """卸载插件"""
        if not self.plugin_manager:
            return {"success": False, "message": "插件管理器未初始化"}
        
        try:
            success = await self.plugin_manager.unload_plugin(plugin_name)
            if success:
                return {"success": True, "message": f"插件 {plugin_name} 卸载成功"}
            else:
                return {"success": False, "message": f"插件 {plugin_name} 卸载失败"}
        except Exception as e:
            self.logger.error(f"卸载插件 {plugin_name} 时出错: {str(e)}", flag="PluginAPI")
            return {"success": False, "message": str(e)}
    
    async def reload_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """重载插件"""
        if not self.plugin_manager:
            return {"success": False, "message": "插件管理器未初始化"}
        
        try:
            success = await self.plugin_manager.reload_plugin(plugin_name)
            if success:
                return {"success": True, "message": f"插件 {plugin_name} 重载成功"}
            else:
                return {"success": False, "message": f"插件 {plugin_name} 重载失败"}
        except Exception as e:
            self.logger.error(f"重载插件 {plugin_name} 时出错: {str(e)}", flag="PluginAPI")
            return {"success": False, "message": str(e)}
    
    async def list_plugins(self) -> List[Dict[str, Any]]:
        """获取插件列表"""
        if not self.plugin_manager:
            return []
        
        return self.plugin_manager.get_plugin_list()
    
    async def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """获取插件信息"""
        if not self.plugin_manager:
            return None
        
        return self.plugin_manager.get_plugin_info(plugin_name)


# 创建全局实例
Plugin_Api = PluginAPI()