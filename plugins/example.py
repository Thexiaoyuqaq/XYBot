from utils.Api.Command_Api import Api

Plugin_Info = {
    'name': '示例插件',
    'author': 'xxx',
    'version': '1.0.0'
}

class Plugin:
    def get_plugin_info(self):
        return Plugin_Info

    async def GroupMessage(self, messageApi, event_original):
        """处理群消息事件"""
        group_id = await messageApi.Get_Group_GroupID()  # 获取群聊ID
        user_id = await messageApi.Get_Sender_UserID()  # 获取用户ID
        message = await messageApi.Get_Message_Content()  # 获取消息内容
        message_id = await messageApi.Get_Message_ID()  # 获取消息ID

        # 示例：如果消息内容为 "1"，则发送 "1"
        if message == "1":
            await Api.send_group_message(group_id, "1")

        # 示例2：如果消息内容为 "2"，则回复发送 "2"  message_id 为空时 则不进行reply回复
        if message == "2":
            await Api.send_group_message(group_id, "2", message_id)

    async def GroupIncrease(self, messageApi, event_original):
        """处理加群事件"""
        group_id = await messageApi.Get_Request_GroupID()  # 获取群聊ID
        user_id = await messageApi.Get_Request_UserID()  # 获取用户ID
        welcome_message = f"欢迎 {await messageApi.Get_Sender_NickName()} 加入群聊！"
        
        # 发送欢迎消息
        await Api.send_group_message(group_id, welcome_message)

    async def GroupDecrease(self, messageApi, event_original):
        """处理退群事件"""
        group_id = await messageApi.Get_Group_GroupID()  # 获取群聊ID
        user_id = await messageApi.Get_Operator_UserID()  # 获取操作用户ID
        goodbye_message = f"用户 {await messageApi.Get_Sender_NickName()} 已离开群聊，再见！"
        
        # 发送退群消息
        await Api.send_group_message(group_id, goodbye_message)

