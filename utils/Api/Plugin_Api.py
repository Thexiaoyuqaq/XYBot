import asyncio
import traceback
from utils.Manager.Log_Manager import Log
from Global.Global import GlobalVal

# 初始化日志记录器
logger = Log()

class APIWrapper:
    """
    用于处理与插件的 API 交互的包装类。
    """

    async def run_plugin_method(self, plugin, method, *args):
        """异步运行插件的特定方法。"""
        if hasattr(plugin, method) and callable(getattr(plugin, method)):
            try:
                await getattr(plugin, method)(*args)
            except Exception:
                plugin_name = plugin.get_plugin_info().get('name', plugin.__class__.__name__)
                logger.error(
                    f"插件 {plugin_name} 执行 {method} 时出现错误:\n{traceback.format_exc()}",
                    flag=plugin_name
                )

    async def run_plugins(self, method_name, *args):
        """异步运行所有插件的指定方法。"""
        tasks = [
            asyncio.create_task(self.run_plugin_method(plugin, method_name, *args))
            for _, plugin in GlobalVal.plugin_list
        ]
        await asyncio.gather(*tasks)

    # -------------------- 事件处理逻辑 --------------------

    async def handle_event(self, event_type, message):
        """
        通用事件处理方法，动态调用插件对应的事件处理逻辑。

        参数:
            event_type: 事件类型（如 "GroupMessage", "Notice_GroupIncrease" 等）。
            message: 事件相关的消息数据。
        """
        message_api = self.Message_Builder(message)
        await self.run_plugins(event_type, message_api, message)

    # -------------------- 消息构建器 --------------------

    class Message_Builder:
        """构建消息的辅助类，用于从消息中提取常用字段。"""

        def __init__(self, message):
            self.message = message

        async def Get(self, *keys, default=None):
            """通用获取方法，避免 KeyError。"""
            data = self.message
            for key in keys:
                data = data.get(key, {})
            return data or default

        async def Get_Group_GroupID(self):
            return await self.Get("group", "group_id")

        async def Get_Group_GroupName(self):
            return await self.Get("group", "group_name")

        async def Get_Sender_UserID(self):
            return await self.Get("sender", "user_id")
        
        async def Get_Sender_UserRole(self):
            return await self.Get("sender", "user_role")

        async def Get_Sender_NickName(self):
            return await self.Get("sender", "user_nickname")

        async def Get_Sender_UserCard(self):
            return await self.Get("sender", "user_card")
        
        async def Get_Message_Message(self):
            """兼容旧插件的调用方式，获取消息内容。"""
            return await self.Get_Message_Content()

        async def Get_Message_Content(self):
            """新的消息内容获取方法。"""
            return self.message["message"]["message"]

        async def Get_Message_ID(self):
            return await self.Get("message", "message_id")

        async def Get_Message_Time(self):
            return await self.Get("message", "message_time")

        async def Get_Request_GroupID(self):
            return await self.Get("group_id")

        async def Get_Request_UserID(self):
            return await self.Get("user_id")

        async def Get_Request_Comment(self):
            return await self.Get("comment")

        async def Get_Request_Flag(self):
            return await self.Get("flag")

        async def Get_User_JoinType(self):
            return await self.Get("event", "sub_type")

        async def Get_Event_Time(self):
            return await self.Get("event", "time")

        async def Get_Operator_UserID(self):
            return await self.Get("event", "operator_id")

    # -------------------- 插件事件接口 --------------------

    async def Plugins_Group_Message(self, message):
        """处理群消息事件。"""
        await self.handle_event("GroupMessage", message)

    async def Plugins_Private_Message(self, message):
        """处理私聊消息事件。"""
        await self.handle_event("PrivateMessage", message)

    async def Plugins_Request_Friend(self, message):
        """处理好友请求事件。"""
        await self.handle_event("Request_Friend", message)

    async def Plugins_Request_Group(self, message):
        """处理群聊申请事件。"""
        await self.handle_event("Request_Group", message)

    async def Plugins_Notice_GroupIncrease(self, message):
        """处理群成员加入通知事件。"""
        await self.handle_event("Notice_GroupIncrease", message)

    async def Plugins_Notice_GroupDecrease(self, message):
        """处理群成员减少通知事件。"""
        await self.handle_event("Notice_GroupDecrease", message)

    async def Plugins_Start(self):
        """运行所有插件的 Start 方法。"""
        await self.run_plugins("Start")

    async def Plugins_Stop(self):
        """运行所有插件的 Stop 方法。"""
        await self.run_plugins("Stop")


# 实例化 APIWrapper
Plugin_Api = APIWrapper()
