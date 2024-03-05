from utils.Manager.Log_Manager import Log
from utils.Api.Command_Api import *


async def cmd_Log(event_Post_Type, event_original):
    logger = Log()

    if event_Post_Type == "notice":
        logger.info(message="[事件]" + str(event_original), flag="Log")
    if event_Post_Type == "消息":
        event_Message_From = event_original["message_type"]

        if event_Message_From == "群聊":
            log_message_sender_nickname = event_original.get("sender", {}).get(
                "user_nickname", ""
            )
            log_message_sender_userid = event_original.get("sender", {}).get(
                "user_id", 0
            )
            log_message_sender_role = event_original.get("sender", {}).get(
                "user_role", ""
            )
            log_message_group_groupid = event_original.get("group", {}).get(
                "group_id", 0
            )
            log_message_group_groupname = event_original.get("group", {}).get(
                "group_name", ""
            )
            log_message_message_message = event_original.get("message", {}).get(
                "message", ""
            )
            log_message_message_message_id = event_original.get("message", {}).get(
                "message_id", ""
            )

            if event_original["sender"]["user_card"]:
                log_message_sender_nickname = event_original["sender"]["user_card"]

            logger.info(
                message=f"[消息][群聊] {log_message_group_groupname}({log_message_group_groupid}) [{log_message_sender_role}] {log_message_sender_nickname}({log_message_sender_userid}): {log_message_message_message} ({log_message_message_message_id})",
                flag="Log",
            )

        elif event_Message_From == "好友":
            log_message_sender_nickname = event_original.get("sender", {}).get(
                "user_nickname", ""
            )
            log_message_sender_userid = event_original.get("sender", {}).get(
                "user_id", 0
            )
            log_message_message_message = event_original.get("message", {}).get(
                "message", ""
            )
            log_message_message_message_id = event_original.get("message", {}).get(
                "message_id", ""
            )

            logger.info(
                message=f"[消息][好友] {log_message_sender_nickname}({log_message_sender_userid})：{log_message_message_message}",
                flag="Log",
            )
