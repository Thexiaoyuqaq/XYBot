from utils.Manager.Log_Manager import Log

async def log_message_event(logger, event_original, message_type):
    """Log message events with full details."""
    sender = event_original.get("sender", {})
    message = event_original.get("message", {})
    group = event_original.get("group", {})

    nickname = sender.get("user_card", "").strip() or sender.get("user_nickname", "")
    user_id = sender.get("user_id", 0)
    message_content = message.get("message", "")
    message_id = message.get("message_id", "")

    if message_type == "group_message":
        role = sender.get("user_role", "")
        group_id = group.get("group_id", 0)
        group_name = group.get("group_name", "")
        logger.info(
            message=f"[消息][群聊] {group_name}({group_id}) [{role}] {nickname}({user_id}): {message_content} ({message_id})",
            flag="Log",
        )
    elif message_type == "friend_message":
        logger.info(
            message=f"[消息][好友] {nickname}({user_id}): {message_content} ({message_id})",
            flag="Log",
        )
    else:
        logger.info(f"[消息][未知] {event_original}", flag="Log")
