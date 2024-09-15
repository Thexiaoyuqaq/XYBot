from utils.Manager.Log_Manager import Log

async def log_notice_event(logger, event_original):
    notice_type = event_original.get("notice_type", "")
    event = event_original.get("event", {})
    
    if notice_type == "group_upload":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        file = event.get("file", {})
        file_name = file.get("name", "未知文件")
        logger.info(f"[事件][群聊][上传] ({group_id}) {user_id} 上传了文件 {file_name}", flag="Log")
    
    elif notice_type == "group_admin":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        sub_type = event.get("sub_type", "")
        action = "设置管理员" if sub_type == "set" else "取消管理员"
        logger.info(f"[事件][群聊][管理] ({group_id}) {user_id} {action}", flag="Log")

    elif notice_type == "group_decrease":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        operator_id = event.get("operator_id", "")
        sub_type = event.get("sub_type", "")
        action = "主动退群" if sub_type == "leave" else "被踢出群聊" if sub_type == "kick" else "登录号被踢出"
        logger.info(f"[事件][群聊][减少] ({group_id}) {operator_id} {action} {user_id}", flag="Log")

    elif notice_type == "group_increase":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        operator_id = event.get("operator_id", "")
        sub_type = event.get("sub_type", "")
        action = "管理员同意入群" if sub_type == "approve" else "管理员邀请入群"
        logger.info(f"[事件][群聊][增加] ({group_id}) {operator_id} {action} {user_id}", flag="Log")

    elif notice_type == "group_ban":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        operator_id = event.get("operator_id", "")
        sub_type = event.get("sub_type", "")
        action = "禁言" if sub_type == "ban" else "解除禁言"
        duration = event.get("duration", "无")
        logger.info(f"[事件][群聊][禁言] ({group_id}) {operator_id} {action} {user_id}, 时长: {duration}秒", flag="Log")

    elif notice_type == "friend_add":
        user_id = event.get("user_id", "")
        logger.info(f"[事件][好友][添加] 新添加好友: {user_id}", flag="Log")

    elif notice_type == "group_recall":
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        operator_id = event.get("operator_id", "")
        message_id = event.get("message_id", "")
        logger.info(f"[事件][群聊][撤回] ({group_id}) {user_id} 撤回了消息 {message_id}", flag="Log")

    elif notice_type == "friend_recall":
        user_id = event.get("user_id", "")
        message_id = event.get("message_id", "")
        logger.info(f"[事件][好友][撤回] 好友: {user_id} 撤回了消息 {message_id}", flag="Log")

    elif notice_type == "notify":
        print(event)

        # #{
        #                 "sub_type": bot_Message_json.get("sub_type", "未知"),  # 类型
        #                 "action_text": bot_Message_json.get(
        #                     "action", "戳了戳"
        #                 ),  # 戳一戳的文字
        #                 "action_suffix": bot_Message_json.get(
        #                     "suffix", ""
        #                 ),  # 戳一戳的附加文字
        #                 "user_id": bot_Message_json.get("user_id", 0),  # 戳的用户
        #                 "target_id": bot_Message_json.get("target_id", 0),  # 被戳用户
        #                 "group_id": bot_Message_json.get("group_id", 0),  # 事件群号
        #                 "time": bot_Message_json.get(
        #                     "time", 0
        #                 ),  # 事件发生的时间戳，数字类型
        #             }

        sub_type = event.get("sub_type", "")
        group_id = event.get("group_id", "")
        user_id = event.get("user_id", "")
        target_id = event.get("target_id", "")
        action = event.get("action_text", "")
        suffix = event.get("action_suffix", "")

        
        if sub_type == "poke":
            logger.info(f"[事件][群聊][戳一戳] ({group_id}) {user_id}{action}{target_id}{suffix}", flag="Log")
        elif sub_type == "lucky_king":
            logger.info(f"[事件][群聊][红包运气王] ({group_id}) 红包发送者: {user_id} 运气王: {target_id}", flag="Log")
        elif sub_type == "honor":

            honor_type = event.get("honor_type", "")
            honor_action = {
                "talkative": "群聊之火",
                "performer": "龙王",
                "emotion": "快乐源泉"
            }.get(honor_type, "未知荣誉")
            logger.info(f"[事件][群聊][荣誉变更] ({group_id}) 成员: {user_id} 荣誉: {honor_action}", flag="Log")

    else:
        logger.info(f"[事件][未知] {event_original}", flag="Log")
