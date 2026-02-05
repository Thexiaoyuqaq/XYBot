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
        group_id = await messageApi.get_group_id()  # 获取群聊ID
        user_id = await messageApi.get_sender_id()  # 获取用户ID
        message = await messageApi.get_message_content()  # 获取消息内容
        message_id = await messageApi.get_message_id()  # 获取消息ID

        # 示例：如果消息内容为 "1"，则发送 "1"
        if message == "1":
            await Api.send_group_message(group_id, "1")

        # 示例2：如果消息内容为 "2"，则回复发送 "2"  message_id 为空时则不进行reply回复
        if message == "2":
            await Api.send_group_message(group_id, "2", message_id)

    async def PrivateMessage(self, messageApi, event_original):
        """处理私聊消息事件"""
        user_id = await messageApi.get_sender_id()  # 获取用户ID
        message = await messageApi.get_message_content()  # 获取消息内容
        message_id = await messageApi.get_message_id()  # 获取消息ID
        nickname = await messageApi.get_sender_nickname()  # 获取用户昵称

        # 示例1：如果消息内容为 "hello"，则回复 "你好！"
        if message == "hello":
            await Api.send_private_message(user_id, f"你好，{nickname}！")

        # 示例2：如果消息内容为 "help"，则回复发送帮助信息
        if message == "help":
            help_text = "这是一个示例插件，可用命令：\nhello - 打招呼\nhelp - 显示帮助"
            await Api.send_private_message(user_id, help_text, message_id)

        # 示例3：回声功能 - 重复用户发送的消息
        if message.startswith("echo "):
            echo_content = message[5:]  # 去掉 "echo " 前缀
            await Api.send_private_message(user_id, f"你说：{echo_content}")

    async def Request_Friend(self, messageApi, event_original):
        """处理好友请求事件"""
        user_id = await messageApi.get_sender_id()  # 获取请求用户ID
        comment = await messageApi.get_request_comment()  # 获取验证消息
        flag = await messageApi.get_request_flag()  # 获取请求标识

        # 示例1：自动同意所有好友请求
        # await Api.set_friend_add_request(flag, approve=True)

        # 示例2：自动同意包含特定关键词的好友请求
        if comment and "加好友" in comment:
            await Api.set_friend_add_request(flag, approve=True, remark="新朋友")
            # 同意后发送欢迎消息
            await Api.send_private_message(user_id, "你好！我已通过你的好友申请。")
        else:
            # 拒绝请求
            await Api.set_friend_add_request(flag, approve=False)

        # 示例3：根据验证消息内容决定是否同意
        # 如果验证消息包含"邀请码"，则同意并备注
        if comment and "邀请码:123456" in comment:
            await Api.set_friend_add_request(flag, approve=True, remark="邀请码用户")

    async def Request_Group(self, messageApi, event_original):
        """处理加群请求事件"""
        group_id = await messageApi.get_group_id()  # 获取群聊ID
        user_id = await messageApi.get_sender_id()  # 获取请求用户ID
        comment = await messageApi.get_request_comment()  # 获取验证消息
        flag = await messageApi.get_request_flag()  # 获取请求标识
        request_type = await messageApi.get_request_type()  # 获取请求类型（添加/邀请）

        # 示例1：自动同意所有加群请求
        # await Api.set_group_add_request(flag, request_type, approve=True)

        # 示例2：根据验证消息决定是否同意
        if comment and "我想加入" in comment:
            # 同意加群请求
            await Api.set_group_add_request(flag, request_type, approve=True)
            # 注意：此时用户还未入群，无法直接发送欢迎消息
            # 欢迎消息应该在 Notice_GroupIncrease 事件中发送
        else:
            # 拒绝加群请求，并给出原因
            await Api.set_group_add_request(
                flag, 
                request_type, 
                approve=False, 
                reason="请填写正确的验证消息"
            )

        # 示例3：根据请求类型（添加/邀请）分别处理
        if request_type == "添加":
            # 用户主动申请加群
            if comment and len(comment) > 10:  # 验证消息长度大于10才同意
                await Api.set_group_add_request(flag, request_type, approve=True)
            else:
                await Api.set_group_add_request(
                    flag, 
                    request_type, 
                    approve=False,
                    reason="请填写详细的验证消息"
                )
        elif request_type == "邀请":
            # 机器人被邀请入群，自动同意
            await Api.set_group_add_request(flag, request_type, approve=True)

    async def Notice_GroupIncrease(self, messageApi, event_original):
        """处理加群事件"""
        group_id = await messageApi.get_group_id()  # 获取群聊ID
        user_id = await messageApi.get_sender_id()  # 获取用户ID
        nickname = await messageApi.get_sender_nickname()  # 获取用户昵称
        join_type = await messageApi.get_event_sub_type()  # 获取加入类型（管理员同意/邀请）
        
        # 示例1：发送基础欢迎消息
        welcome_message = f"欢迎 {nickname} 加入群聊！"
        await Api.send_group_message(group_id, welcome_message)

        # 示例2：根据加入类型发送不同的欢迎消息
        if join_type == "管理员同意入群":
            welcome_message = f"欢迎新成员 {nickname}！你的申请已通过审核。"
        elif join_type == "管理员邀请入群":
            welcome_message = f"欢迎 {nickname}！感谢管理员的邀请。"
        
        await Api.send_group_message(group_id, welcome_message)

        # 示例3：发送群规则
        rules = "请遵守群规则：\n1. 文明聊天\n2. 禁止广告\n3. 互相尊重"
        await Api.send_group_message(group_id, rules)

    async def Notice_GroupDecrease(self, messageApi, event_original):
        """处理退群事件"""
        group_id = await messageApi.get_group_id()  # 获取群聊ID
        user_id = await messageApi.get_sender_id()  # 获取退群用户ID
        operator_id = await messageApi.get_operator_id()  # 获取操作者ID
        nickname = await messageApi.get_sender_nickname()  # 获取用户昵称
        leave_type = await messageApi.get_event_sub_type()  # 获取离开类型
        
        # 示例1：根据离开类型发送不同的消息
        if leave_type == "主动退群":
            goodbye_message = f"用户 {nickname} 已离开群聊，祝一切顺利！"
        elif leave_type == "成员被踢出":
            goodbye_message = f"用户 {nickname} 被移出群聊。"
        elif leave_type == "被踢出群聊":
            goodbye_message = "机器人被移出群聊。"
            # 注意：如果是机器人自己被踢，这条消息将无法发送
        else:
            goodbye_message = f"用户 {nickname} 已离开群聊。"
        
        await Api.send_group_message(group_id, goodbye_message)

        # 示例2：记录退群信息（可以保存到数据库）
        # 这里仅作为示例打印
        print(f"群 {group_id} 的成员 {user_id}({nickname}) 离开了，类型：{leave_type}")

    async def Start(self):
        """处理插件加载事件"""
        print("示例插件加载成功")
        print("已注册的事件处理器：")
        print("- GroupMessage: 群消息处理")
        print("- PrivateMessage: 私聊消息处理")
        print("- Request_Friend: 好友请求处理")
        print("- Request_Group: 加群请求处理")
        print("- Notice_GroupIncrease: 成员加群通知")
        print("- Notice_GroupDecrease: 成员退群通知")

    async def Stop(self):
        """处理插件卸载事件"""
        print("示例插件卸载成功")
