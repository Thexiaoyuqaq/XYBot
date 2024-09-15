
from utils.Api.Command_Api import *

Plugin_Info = {
    'name': '示例插件',
    'author': 'xxx',
    'version': '1.0.0'
}

class Plugin:
    def get_plugin_info(self):
       return Plugin_Info

    async def GroupMessage(self,messageApi, event_original):
        #群消息事件处理逻辑
        #获取数据
        group_id = await messageApi.Get_Group_GroupID() #获取群聊ID
        user_id = await messageApi.Get_Sender_UserID()  # 获取用户ID
        message = await messageApi.Get_Message_Message()  # 获取消息内容
        message_id = await messageApi.Get_Message_MessageID()  # 获取消息ID

        if message == "1":
           asyncio.create_task(Api.send_Groupmessage(group_id,message_id, "1" ,True))