async def log_request_event(logger, event_original, type = "request"):
    request_type = event_original.get("request_type", "")
    if request_type == "群聊请求":
        data = event_original.get("request", {})
        group_id = data.get("group_id", "") # 群号
        user_id = data.get("user_id", "") # 用户id
        comment = data.get("comment", "") # 请求理由
        flag = data.get("flag", "") # 请求flag (id)
        logger.info(f"[请求][群聊][申请] {user_id} 申请加入 {group_id} 群聊，理由: {comment}", flag="Log")
    elif request_type == "好友请求":
        data = event_original.get("request", {})
        user_id = data.get("user_id", "") # 用户id
        comment = data.get("comment", "") # 请求理由
        flag = data.get("flag", "") # 请求flag (id)

        logger.info(f"[请求][好友][申请] {user_id} 申请添加好友，理由: {comment}", flag="Log")