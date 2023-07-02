from Api import *


class Plugin:
    async def Notice_Group_join(self, event_original):
        # 加群事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        await send_Groupmessage(group_id, 0, f"欢迎新成员加入，用户ID: {user_id}",False)

    async def Start(self):
        # 启动事件处理逻辑
        #await send_Groupmessage("123456789", 0, "机器人已启动",False)
        pass

    async def Notice_Group_leave(self, event_original):
        # 退群事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        await send_Groupmessage(group_id, 0, f"群成员离开，用户ID: {user_id}",False)

    async def Request(self, event_request_from, event_original):
        # 请求事件处理逻辑
        if event_request_from == "friend":
            # 好友请求处理逻辑
            flag = event_original["flag"]  # 获取Flag
            await set_GroupRequest(flag, True)
        elif event_request_from == "group":
            # 加群请求处理逻辑
            flag = event_original["flag"]  # 获取Flag
            await set_GroupRequest(flag, True)

    async def GroupMessage(self, event_original):
        # 群消息事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        message = event_original["message"]  # 获取消息内容
        message_id = event_original["message_id"]  # 获取消息内容
        await send_Groupmessage(group_id,message_id, "收到消息Test" ,True)

    async def FriendMessage(self, event_original):
        # 好友消息事件处理逻辑
        user_id = event_original["user_id"]  # 获取用户ID
        message = event_original["message"]  # 获取消息内容
        #await send_PrivateMessage(user_id, f"收到好友消息，消息内容: {message}")
        await send_FriendMessage(user_id,f"收到好友消息，消息内容: {message}")
