from Api import get_group_info
from LogSys import Log


async def cmd_Log(event_Post_Type, event_original):
    """
    处理日志命令的函数。

    Args:
        event_Post_Type (str): 事件的类型。
        event_original (dict): 原始事件数据。

    Returns:
        None
    """
    logger = Log()

    if event_Post_Type == "notice":
        logger.info(message="[信息][事件][接收]" + str(event_original))

    if event_Post_Type == "message":
        event_Message_From = event_original["message_type"]

        if event_Message_From == "group":
            message_info = {
                "message_type": "群聊",
                "user_id": event_original["user_id"],
                "sender": {
                    "nickname": event_original["sender"]["nickname"],
                    "role": event_original["sender"]["role"]
                },
                "message": event_original["message"],
                "group_id": event_original["group_id"],
                "message_id": event_original["message_id"]
            }
            group_info = await get_group_info(event_original["group_id"])
            group_name = group_info["data"]["group_name"]

            logger.info(message=f"[消息][群聊] {group_name}({event_original['group_id']}) [{message_info['sender']['role']}] {message_info['sender']['nickname']}({message_info['user_id']}): {message_info['message']} ({message_info['message_id']})", flag="Log")

        if event_Message_From == "private":
            message_info = {
                "message_type": "好友",
                "user_id": event_original["user_id"],
                "sender": {
                    "nickname": event_original["sender"]["nickname"]
                },
                "message": event_original["message"]
            }

            logger.info(message=f"[消息][好友] {message_info['sender']['nickname']}({message_info['user_id']})：{message_info['message']}", flag="Log")
