from utils.Manager.Log_Manager import Log
from utils.Api.Command_Api import *

async def log_event(logger, event_original, log_type, extra_info=""):
    sender = event_original.get("sender", {})
    message = event_original.get("message", {})
    group = event_original.get("group", {})

    nickname = sender.get("user_card", "").strip() or sender.get("user_nickname", "")

    user_id = sender.get("user_id", 0)
    message_content = message.get("message", "")
    message_id = message.get("message_id", "")

    if log_type == "notice":
        logger.info(message=f"[事件] {event_original}", flag="Log")
    elif log_type == "group_message":
        role = sender.get("user_role", "")
        group_id = group.get("group_id", 0)
        group_name = group.get("group_name", "")
        logger.info(
            message=f"[消息][群聊] {group_name}({group_id}) [{role}] {nickname}({user_id}): {message_content} ({message_id})",
            flag="Log",
        )
    elif log_type == "friend_message":
        logger.info(
            message=f"[消息][好友] {nickname}({user_id}): {message_content} ({message_id})",
            flag="Log",
        )
    elif log_type == "unknown" or log_type == "未知":
        logger.info(message=f"[未知] {event_original}", flag="Log")

async def cmd_Log(post_type, original_event):
    logger = Log()
    if post_type == "事件":
        asyncio.create_task(log_event(logger, original_event, "notice"))
    elif post_type == "消息":
        event_Message_From = original_event.get("message_type", "")
        if event_Message_From == "群聊":
            asyncio.create_task(log_event(logger, original_event, "group_message"))
        elif event_Message_From == "好友":
            asyncio.create_task(log_event(logger, original_event, "friend_message"))
    else:
        asyncio.create_task(log_event(logger, original_event, "unknown"))
