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
        await self.run_plugins("Notice_Group_join", message)

    async def Plugins_Notice_leave(self, message):
        await self.run_plugins("Notice_Group_leave", message)

    async def Plugins_Start(self):
        await self.run_plugins("Start")

    async def Plugins_Stop(self):
        await self.run_plugins("Stop")

Plugin_Api = APIWrapper()
