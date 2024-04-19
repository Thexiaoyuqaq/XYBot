import asyncio
from utils.Manager.Log_Manager import Log
from Global.Global import GlobalVal

logger = Log()

class APIWrapper:
    def __init__(self):
        self.plugin_methods = [
            "GroupMessage",
            "FriendMessage",
            "Request",
            "Notice_Group_join",
            "Notice_Group_leave",
            "Start",
            "Stop",
        ]

    async def run_plugin_method(self, plugin, method, *args):
        if hasattr(plugin, method) and callable(getattr(plugin, method)):
            try:
                await getattr(plugin, method)(*args)
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin.__class__.__name__)

    async def run_plugins(self, method_name, *args):
        tasks = []
        for _, plugin in GlobalVal.plugin_list:
            tasks.append(
                asyncio.create_task(self.run_plugin_method(plugin, method_name, *args))
            )
        await asyncio.gather(*tasks)

    async def Plugins_Group_Message(self, message):
        class Message_Builder:
            def __init__(self, message):
                self.message = message

            async def Get_Group_GroupID(self):
                return self.message["group"]["group_id"]

            async def Get_Group_GroupName(self):
                return self.message["group"]["group_name"]

            async def Get_Sender_User_role(self):
                return self.message["sender"]["role"]

            async def Get_Sender_UserID(self):
                return self.message["sender"]["user_id"]

            async def Get_Sender_NickName(self):
                return self.message["sender"]["user_nickname"]

            async def Get_Message_Message(self):
                return self.message["message"]["message"]

            async def Get_Message_MessageID(self):
                return self.message["message"]["message_id"]

            async def Get_Message_Message_Time(self):
                return self.message["message"]["message_time"]

        message_api = Message_Builder(message)
        await self.run_plugins("GroupMessage", message_api, message)

    async def Plugins_Friend_Message(self, message):
        await self.run_plugins("FriendMessage", message)

    async def Plugins_Request(self, message):
        await self.run_plugins("Request", message)

    async def Plugins_Notice_join(self, message):
        class Message_Builder:
            def __init__(self, message):
                self.message = message
            
            #获取事件群号
            async def Get_Group_GroupID(self):
                return self.message["event"]["group_id"]

            #获取事件加入类型：
            # 返回： invite：邀请入群 approve：主动入群
            async def Get_User_JoinType(self):  
                return self.message["event"]["sub_type"]
            
            # 获取事件人QQ号
            # 也就是 申请人/被邀请人QQ号
            async def Get_Sender_UserID(self):  

                return self.message["event"]["user_id"]
            # 操作人QQ号
            # 也就是 处理人QQ号
            # 在用户主动申请 则为审核管理的qq
            # 在用户被拉入群聊 则为拉人的用户qq
            async def Get_Operator_UserID(self):
                return self.message["event"]["operator_id"]
            #事件时间 
            async def Get_Event_Time(self):
                return self.message["event"]["time"]
        message_api = Message_Builder(message)
        await self.run_plugins("Notice_Group_join", message_api  ,message)

    async def Plugins_Notice_leave(self, message):
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
        await self.run_plugins("Notice_Group_leave", message_api, message)

    async def Plugins_Start(self):
        await self.run_plugins("Start")

    async def Plugins_Stop(self):
        await self.run_plugins("Stop")

Plugin_Api = APIWrapper()
