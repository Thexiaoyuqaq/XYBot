# utils/Manager/Event_Manager.py
import asyncio
import json
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum

from utils.Manager.Log_Manager import Log
from utils.Manager.Message_Manager import MessageNew
from Global.Global import GlobalVal


class EventType(Enum):
    """事件类型枚举"""
    MESSAGE = "消息"
    REQUEST = "请求"
    NOTICE = "事件"
    HEARTBEAT = "心跳包"
    UNKNOWN = "未知"


class MessageType(Enum):
    """消息类型枚举"""
    GROUP = "群聊"
    PRIVATE = "好友"
    UNKNOWN = "未知"


class RequestType(Enum):
    """请求类型枚举"""
    FRIEND = "好友请求"
    GROUP = "群聊请求"
    UNKNOWN = "未知"


class NoticeType(Enum):
    """通知类型枚举"""
    GROUP_INCREASE = "群成员增加"
    GROUP_DECREASE = "群成员减少"
    GROUP_ADMIN = "群管理员变动"
    GROUP_UPLOAD = "群文件上传"
    GROUP_BAN = "群禁言"
    UNKNOWN = "未知"


@dataclass
class EventContext:
    """事件上下文"""
    event_type: EventType
    raw_event: Dict[str, Any]
    processed_event: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: asyncio.get_event_loop().time())
    
    @property
    def message_type(self) -> Optional[MessageType]:
        """获取消息类型"""
        if self.event_type == EventType.MESSAGE:
            msg_type = self.processed_event.get("message_type", "")
            if msg_type == "群聊":
                return MessageType.GROUP
            elif msg_type == "好友":
                return MessageType.PRIVATE
        return None
    
    @property
    def request_type(self) -> Optional[RequestType]:
        """获取请求类型"""
        if self.event_type == EventType.REQUEST:
            req_type = self.processed_event.get("request_type", "")
            if req_type == "好友请求":
                return RequestType.FRIEND
            elif req_type == "群聊请求":
                return RequestType.GROUP
        return None
    
    @property
    def notice_type(self) -> Optional[NoticeType]:
        """获取通知类型"""
        if self.event_type == EventType.NOTICE:
            notice = self.processed_event.get("notice_type", "")
            notice_map = {
                "群成员增加": NoticeType.GROUP_INCREASE,
                "群成员减少": NoticeType.GROUP_DECREASE,
                "群管理员变动": NoticeType.GROUP_ADMIN,
                "群文件上传": NoticeType.GROUP_UPLOAD,
                "群禁言": NoticeType.GROUP_BAN,
            }
            return notice_map.get(notice, NoticeType.UNKNOWN)
        return None


class EventManager:
    """事件管理器，负责事件的分发和处理"""
    
    def __init__(self):
        self.logger = Log()
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._middleware: List[Callable] = []
        self._running_tasks: List[asyncio.Task] = []
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._processing = False
        
    def register_middleware(self, middleware: Callable) -> None:
        """注册中间件"""
        self._middleware.append(middleware)
        
    def unregister_middleware(self, middleware: Callable) -> None:
        """注销中间件"""
        if middleware in self._middleware:
            self._middleware.remove(middleware)
    
    async def _run_middleware(self, context: EventContext) -> bool:
        """运行中间件链"""
        for middleware in self._middleware:
            try:
                result = await middleware(context)
                if result is False:  # 中间件返回False则停止处理
                    return False
            except Exception as e:
                self.logger.error(f"中间件执行错误: {e}", flag="EventManager")
        return True
    
    async def process_event(self, raw_event: Dict[str, Any]) -> None:
        """处理原始事件"""
        try:
            # 解析事件类型
            post_type = raw_event.get("post_type", "")
            
            # 处理并格式化事件
            processed_event = await MessageNew(raw_event)
            if not processed_event:
                return
            
            # 确定事件类型
            event_type = self._get_event_type(processed_event.get("post_type", ""))
            
            # 跳过心跳包
            if event_type == EventType.HEARTBEAT:
                return
            
            # 创建事件上下文
            context = EventContext(
                event_type=event_type,
                raw_event=raw_event,
                processed_event=processed_event
            )
            
            # 运行中间件
            if not await self._run_middleware(context):
                return
            
            # 记录日志
            await self._log_event(context)
            
            # 分发事件到插件
            await self._dispatch_event(context)
            
        except Exception as e:
            self.logger.error(f"事件处理错误: {e}", flag="EventManager")
    
    def _get_event_type(self, post_type: str) -> EventType:
        """获取事件类型"""
        type_map = {
            "消息": EventType.MESSAGE,
            "请求": EventType.REQUEST,
            "事件": EventType.NOTICE,
            "心跳包": EventType.HEARTBEAT,
        }
        return type_map.get(post_type, EventType.UNKNOWN)
    
    async def _log_event(self, context: EventContext) -> None:
        """记录事件日志"""
        from Log import cmd_Log
        await cmd_Log(
            context.processed_event.get("post_type", ""),
            context.processed_event
        )
    
    async def _dispatch_event(self, context: EventContext) -> None:
        """分发事件到插件系统"""
        try:
            # 获取插件API
            from utils.Api.Plugin_Api import Plugin_Api
            
            # 根据事件类型分发
            if context.event_type == EventType.MESSAGE:
                await self._dispatch_message_event(context, Plugin_Api)
            elif context.event_type == EventType.REQUEST:
                await self._dispatch_request_event(context, Plugin_Api)
            elif context.event_type == EventType.NOTICE:
                await self._dispatch_notice_event(context, Plugin_Api)
                
        except Exception as e:
            self.logger.error(f"事件分发错误: {e}", flag="EventManager")
    
    async def _dispatch_message_event(self, context: EventContext, api) -> None:
        """分发消息事件"""
        if context.message_type == MessageType.GROUP:
            await api.Plugins_Group_Message(context.processed_event)
        elif context.message_type == MessageType.PRIVATE:
            await api.Plugins_Private_Message(context.processed_event)
    
    async def _dispatch_request_event(self, context: EventContext, api) -> None:
        """分发请求事件"""
        if context.request_type == RequestType.FRIEND:
            await api.Plugins_Request_Friend(context.processed_event)
        elif context.request_type == RequestType.GROUP:
            await api.Plugins_Request_Group(context.processed_event)
    
    async def _dispatch_notice_event(self, context: EventContext, api) -> None:
        """分发通知事件"""
        if context.notice_type == NoticeType.GROUP_INCREASE:
            await api.Plugins_Notice_GroupIncrease(context.processed_event)
        elif context.notice_type == NoticeType.GROUP_DECREASE:
            await api.Plugins_Notice_GroupDecrease(context.processed_event)
    
    def cleanup_tasks(self) -> None:
        """清理运行中的任务"""
        for task in self._running_tasks:
            if not task.done():
                task.cancel()
        self._running_tasks.clear()