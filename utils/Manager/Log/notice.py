async def log_notice_event(logger, event_original):
    notice_type = event_original.get("notice_type", "")
    event = event_original.get("event", {})
    
    group_id = event.get("group_id", "")
    user_id = event.get("user_id", "")
    operator_id = event.get("operator_id", "")
    
    log_message = f"[事件][群聊] ({group_id}) {user_id}"

    if notice_type == "群文件上传":
        file_name = event.get("file", {}).get("name", "未知文件")
        logger.info(f"{log_message} 上传了文件 {file_name}", flag="Log")
    
    elif notice_type == "群管理员变动":
        sub_type = event.get("sub_type", "")
        action = "设置管理员" if sub_type == "set" else "取消管理员"
        logger.info(f"{log_message} {action}", flag="Log")

    elif notice_type == "群成员减少":
        sub_type = event.get("sub_type", "")
        action = "主动退群" if sub_type == "leave" else "被踢出群聊" if sub_type == "kick" else "登录号被踢出"
        logger.info(f"[事件][群聊][减少] {user_id} {action} {group_id}  操作人： {operator_id}", flag="Log")

    elif notice_type == "群成员增加":
        sub_type = event.get("sub_type", "")
        action = "被管理员同意入群" if sub_type == "approve" else "被管理员邀请入群"
        logger.info(f"[事件][群聊][增加] {user_id} {action} {group_id}  操作人： {operator_id} ", flag="Log")

    elif notice_type == "群禁言":
        sub_type = event.get("sub_type", "")
        action = "禁言" if sub_type == "ban" else "解除禁言"
        duration = event.get("duration", "无")
        logger.info(f"[事件][群聊][禁言] ({group_id}) {operator_id} {action} {user_id}, 时长: {duration}秒", flag="Log")

    elif notice_type == "群消息撤回":
        message_id = event.get("message_id", "")
        tip = event.get("tip", "")
        logger.info(f"[事件][群聊][撤回] ({group_id}) {user_id} 撤回了一条消息,{tip}  ——({message_id})", flag="Log")

    elif notice_type == "好友消息撤回":
        message_id = event.get("message_id", "")
        logger.info(f"[事件][好友][撤回] 好友: {user_id} 撤回了消息 {message_id}", flag="Log")

    elif notice_type == "通知":
        sub_type = event.get("sub_type", "")
        if sub_type == "戳一戳":
            action = event.get("action_text", "")
            target_id = event.get("target_id", "")
            suffix = event.get("action_suffix", "")
            logger.info(f"[事件][群聊][戳一戳] ({group_id}) {user_id} {action} {target_id} {suffix}", flag="Log")
        elif sub_type == "群荣誉变更":
            honor_type = event.get("honor_type", "")
            honor_action = {
                "talkative": "群聊之火",
                "performer": "龙王",
                "emotion": "快乐源泉"
            }.get(honor_type, "未知荣誉")
            logger.info(f"[事件][群聊][荣誉变更] ({group_id}) 成员: {user_id} 荣誉: {honor_action}", flag="Log")

    else:
        logger.info(f"[事件][未知] {event_original}", flag="Log")
