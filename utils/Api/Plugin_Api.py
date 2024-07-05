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
        """
        异步运行插件的特定方法。

        参数:
            plugin: 插件对象。
            method: 要调用的方法。
            *args: 要传递给方法的参数。
        """
        if hasattr(plugin, method) and callable(getattr(plugin, method)):
            try:
                await getattr(plugin, method)(*args)
            except Exception as e:
                plugin_name = plugin.get_plugin_info().get('name', plugin.__class__.__name__)
                traceback_str = traceback.format_exc()
                logger.error(f"错误: {str(traceback_str)}", flag=plugin_name)

    async def run_plugins(self, method_name, *args):
        """
        异步运行所有插件的指定方法。

        参数:
            method_name: 要调用的方法名称。
            *args: 要传递给方法的参数。
        """
        tasks = []
        for _, plugin in GlobalVal.plugin_list:
            tasks.append(
                asyncio.create_task(self.run_plugin_method(plugin, method_name, *args))
            )
        await asyncio.gather(*tasks)

    async def Plugins_Group_Message(self, message):
        """
        处理群消息的插件方法。

        参数:
            message: 消息内容。
        """
        class Message_Builder:
            """
            构建消息的辅助类。
            """
            def __init__(self, message):
                self.message = message

            async def Get_Group_GroupID(self):
                """获取群聊的ID。"""
                return self.message["group"]["group_id"]

            async def Get_Group_GroupName(self):
                """获取群聊的名称。"""
                return self.message["group"]["group_name"]

            async def Get_Sender_User_role(self):
                """获取发送消息的用户角色。"""
                return self.message["sender"]["user_role"]

            async def Get_Sender_UserID(self):
                """获取发送消息的用户ID。"""
                return self.message["sender"]["user_id"]

            async def Get_Sender_NickName(self):
                """获取发送消息的用户昵称。"""
                return self.message["sender"]["user_nickname"]

            async def Get_Message_Message(self):
                """获取消息内容。"""
                return self.message["message"]["message"]

            async def Get_Message_MessageID(self):
                """获取消息ID。"""
                return self.message["message"]["message_id"]

            async def Get_Message_Message_Time(self):
                """获取消息发送时间。"""
                return self.message["message"]["message_time"]

        message_api = Message_Builder(message)
        await self.run_plugins("GroupMessage", message_api, message)

    async def Plugins_Private_Message(self, message):
        """
        处理私聊消息的插件方法。

        参数:
            message: 消息内容。
        """
        class Message_Builder:
            """
            构建消息的辅助类。
            """
            def __init__(self, message):
                self.message = message

            async def Get_Sender_UserID(self):
                """获取发送消息的用户ID。"""
                return self.message["sender"]["user_id"]

            async def Get_Sender_NickName(self):
                """获取发送消息的用户昵称。"""
                return self.message["sender"]["user_nickname"]

            async def Get_Message_Message(self):
                """获取消息内容。"""
                return self.message["message"]["message"]

            async def Get_Message_MessageID(self):
                """获取消息ID。"""
                return self.message["message"]["message_id"]

            async def Get_Message_Message_Time(self):
                """获取消息发送时间。"""
                return self.message["message"]["message_time"]

        message_api = Message_Builder(message)
        await self.run_plugins("PrivateMessage", message_api, message)

    async def Plugins_Request_Friend(self, message):
        """
        处理好友请求的插件方法。

        参数:
            message: 请求消息内容。
        """
        await self.run_plugins("Request_Friend", message)
    
    # 处理群聊申请事件的插件方法
    async def Plugins_Request_Group(self, message):
        """
        处理群聊申请事件的插件方法。

        参数:
            message: 请求消息内容。
        """
        class Message_Builder:
            """
            构建消息的辅助类。
            """
            def __init__(self, message):
                self.message = message

            # 获取请求的群号
            async def Get_Request_GroupID(self):
                """获取请求的群号。"""
                return self.message["group_id"]

            # 获取事件人QQ号：申请人的qq号
            async def Get_Request_UserID(self):  
                """获取事件人的QQ号（申请人）。"""
                return self.message["user_id"]

            # 加群验证消息
            async def Get_Request_Comment(self):
                """获取加群验证消息。"""
                return self.message["comment"]

            # 获取请求时间
            async def Get_Request_Time(self):
                """获取请求时间。"""
                return self.message["time"]

            # 获取请求flag，在操作同意和拒绝时需要用到 flag分为：主动、邀请
            async def Get_Request_Flag(self):
                """获取请求的标志。"""
                return self.message["flag"]
            
        message_api = Message_Builder(message)
        await self.run_plugins("Request_Group", message_api, message)

    async def Plugins_Notice_GroupIncrease(self, message):
        """
        处理群成员加入通知事件的插件方法。

        参数:
            message: 通知消息内容。
        """
        class Message_Builder:
            """
            构建消息的辅助类。
            """
            def __init__(self, message):
                self.message = message
            
            # 获取事件群号
            async def Get_Group_GroupID(self):
                """获取事件群号。"""
                return self.message["event"]["group_id"]

            # 获取事件加入类型：
            # 返回： invite：邀请入群 approve：主动入群
            async def Get_User_JoinType(self):  
                """获取用户加入类型。"""
                return self.message["event"]["sub_type"]
            
            # 获取事件人QQ号
            # 也就是 申请人/被邀请人QQ号
            async def Get_Sender_UserID(self):  
                """获取事件人的QQ号。"""
                return self.message["event"]["user_id"]

            # 操作人QQ号
            # 也就是 处理人QQ号
            # 在用户主动申请 则为审核管理的qq
            # 在用户被拉入群聊 则为拉人的用户qq
            async def Get_Operator_UserID(self):
                """获取操作人的QQ号。"""
                return self.message["event"]["operator_id"]

            # 事件时间 
            async def Get_Event_Time(self):
                """获取事件时间。"""
                return self.message["event"]["time"]

        message_api = Message_Builder(message)
        await self.run_plugins("Notice_GroupIncrease", message_api, message)

    async def Plugins_Notice_GroupDecrease(self, message):
        class Message_Builder:
            def __init__(self, message):
                self.message = message
            
            #获取事件群号
            async def Get_Group_GroupID(self):
                return self.message["event"]["group_id"]

            #获取事件退群类型：
            # 返回： kick：被踢出 leave: 主动退群 kick_me: 自己被踢出
            async def Get_User_LeaveType(self):  
                return self.message["event"]["sub_type"]
            
            # 获取事件人QQ号
            # 也就是 退群用户的QQ号
            async def Get_Sender_UserID(self):  

                return self.message["event"]["user_id"]
            # 操作人QQ号
            # 如果是主动退群，则为退群用户本身
            # 如果是管理员踢出，则为管理员
            async def Get_Operator_UserID(self):
                return self.message["event"]["operator_id"]
            #事件时间 
            async def Get_Event_Time(self):
                return self.message["event"]["time"]
        message_api = Message_Builder(message)
        await self.run_plugins("Notice_GroupDecrease", message_api, message)

    async def Plugins_Start(self):
        await self.run_plugins("Start")

    async def Plugins_Stop(self):
        await self.run_plugins("Stop")

Plugin_Api = APIWrapper()
