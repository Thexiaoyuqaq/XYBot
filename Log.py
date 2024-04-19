from utils.Manager.Log_Manager import Log
from utils.Api.Command_Api import *


async def log_notice(logger, event_original):
    logger.info(message="[事件] " + str(event_original), flag="Log")

async def log_group_message(logger, event_original):
    sender = event_original.get("sender", {})
    group = event_original.get("group", {})
    message = event_original.get("message", {})

    nickname = sender.get("user_card", sender.get("user_nickname", ""))
    user_id = sender.get("user_id", 0)
    role = sender.get("user_role", "")
    group_id = group.get("group_id", 0)
    group_name = group.get("group_name", "")
    message_content = message.get("message", "")
    message_id = message.get("message_id", "")

    logger.info(
        message=f"[消息][群聊] {group_name}({group_id}) [{role}] {nickname}({user_id}): {message_content} ({message_id})",
        flag="Log",
    )

async def log_friend_message(logger, event_original):
    sender = event_original.get("sender", {})
    nickname = sender.get("user_nickname", "")
    user_id = sender.get("user_id", 0)
    message_content = event_original.get("message", {}).get("message", "")
    message_id = event_original.get("message", {}).get("message_id", "")

    logger.info(
        message=f"[消息][好友] {nickname}({user_id}): {message_content}",
        flag="Log",
    )

async def cmd_Log(post_type, original_event):
    logger = Log()

    if post_type == "事件":
        asyncio.create_task(log_notice(logger, original_event))
    elif post_type == "消息":
        event_Message_From = original_event.get("message_type", "")

        if event_Message_From == "群聊":
            asyncio.create_task(log_group_message(logger, original_event))
        elif event_Message_From == "好友":
            asyncio.create_task(log_friend_message(logger, original_event))
