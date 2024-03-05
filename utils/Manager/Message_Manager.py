import json
from utils.Api.Command_Api import Api


async def Message_to_New(bot_Message_json: dict):
    Message_json = {}
    # bot_Message_json = json.loads(bot_Message_json)

    Message_PostType = bot_Message_json.get("post_type", "none")

    if Message_PostType == "message":
        Message_json["post_type"] = "消息"

        Message_MessageType = bot_Message_json.get("message_type", "none")

        if Message_MessageType == "private":
            Message_json["message_type"] = "好友"

            Message_Message = bot_Message_json.get("raw_message", "")
            Message_Sender_UserID = bot_Message_json.get("sender", {}).get("user_id", 0)
            Message_Sender_User_nickname = bot_Message_json.get("sender", {}).get(
                "nickname", ""
            )
            Message_raw_message = bot_Message_json.get("message", {})
            Message_Message_Time = bot_Message_json.get("time", 11451459200)
            Message_MessageID = bot_Message_json.get("message_id", -114514)

            Message_json["message"] = {
                "message": Message_Message,
                "message_id": Message_MessageID,
                "message_time": Message_Message_Time,
                "raw": Message_raw_message,
            }
            Message_json["sender"] = {
                "user_id": Message_Sender_UserID,
                "user_nickname": Message_Sender_User_nickname,
            }

        elif Message_MessageType == "group":
            Message_json["message_type"] = "群聊"

            Message_GroupID = bot_Message_json.get("group_id", 0)
            Message_Message = bot_Message_json.get("raw_message", "")
            Message_Sender_UserID = bot_Message_json.get("sender", {}).get("user_id", 0)
            Message_Sender_User_role = bot_Message_json.get("sender", {}).get(
                "role", "群员"
            )
            Message_Sender_User_card = bot_Message_json.get("sender", {}).get(
                "card", ""
            )
            Message_Sender_User_nickname = bot_Message_json.get("sender", {}).get(
                "nickname", ""
            )
            Message_raw_message = bot_Message_json.get("message", {})
            Message_Message_Time = bot_Message_json.get("time", 11451459200)
            Message_MessageID = bot_Message_json.get("message_id", -114514)

            if Message_Sender_User_role == "owner":
                Message_Sender_User_role = "群主"
            elif Message_Sender_User_role == "admin":
                Message_Sender_User_role = "管理"

            ws_recv_data = await Api.get_group_info(Message_GroupID)

            Message_json["group"] = {
                "group_id": Message_GroupID,
                "group_name": ws_recv_data["group_name"],
                "group_member_count": ws_recv_data["member_count"],
                "group_max_member_count": ws_recv_data["max_member_count"],
            }

            Message_json["message"] = {
                "message": Message_Message,
                "message_id": Message_MessageID,
                "message_time": Message_Message_Time,
                "raw": Message_raw_message,
            }
            Message_json["sender"] = {
                "user_id": Message_Sender_UserID,
                "user_role": Message_Sender_User_role,
                "user_card": Message_Sender_User_card,
                "user_nickname": Message_Sender_User_nickname,
            }
    elif Message_PostType == "meta_event":
        Message_json = bot_Message_json
        Message_json["post_type"] = "心跳包"
    else:
        return None
    return Message_json
