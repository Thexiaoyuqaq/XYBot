from utils.Manager.Log_Manager import Log
from Global.Global import GlobalVal

logger = Log()


class APIWrapper:
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

        messageApi = Message_Builder(message)

        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "GroupMessage") and callable(
                getattr(plugin, "GroupMessage")
            ):
                # try:
                await plugin.GroupMessage(messageApi, message)
             except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][消息][{plugin_name}] 插件缺少 'GroupMessage' 方法，跳过执行。")

    async def Plugins_Friend_Message(self, message):
        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "FriendMessage") and callable(
                getattr(plugin, "FriendMessage")
            ):
                try:
                    await plugin.FriendMessage(message)
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][消息][{plugin_name}] 插件缺少 'FriendMessage' 方法，跳过执行。")

    async def Plugins_Request(self, message):
        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "Request") and callable(getattr(plugin, "Request")):
                try:
                    await plugin.Request(message)
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][事件][请求][{plugin_name}] 插件缺少 'Request' 方法，跳过执行。")

    async def Plugins_Notice_join(self, message):
        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "Notice_Group_join") and callable(
                getattr(plugin, "Notice_Group_join")
            ):
                try:
                    await plugin.Notice_Group_join(message)
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][事件][进群][{plugin_name}] 插件缺少 'Notice_join' 方法，跳过执行。")

    async def Plugins_Notice_leave(self, message):

        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "Notice_Group_leave") and callable(
                getattr(plugin, "Notice_Group_leave")
            ):
                try:
                    await plugin.Notice_Group_leave(message)
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][事件][退群][{plugin_name}] 插件缺少 'Notice_leave' 方法，跳过执行。")

    async def Plugins_Start(self):
        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "Start") and callable(getattr(plugin, "Start")):
                try:
                    await plugin.Start()
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][事件][启动][{plugin_name}] 插件缺少 'Start' 方法，跳过执行。")

    async def Plugins_Stop(self):
        for plugin_name, plugin in GlobalVal.plugin_list:
            if hasattr(plugin, "Stop") and callable(getattr(plugin, "Stop")):
                try:
                    await plugin.Stop()
                except Exception as e:
                    logger.error(f"Error: {str(e)}", flag=plugin_name)
            else:
                pass
                # print(event_Time + f"[警告][插件][跳过][事件][关闭][{plugin_name}] 插件缺少 'Stop' 方法，跳过执行。")


Plugin_Api = APIWrapper()
