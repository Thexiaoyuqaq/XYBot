from typing import Dict
from utils.Api.Command_Api import Api

async def format_message(bot_Message_json: Dict) -> Dict:
    def get_sender_info() -> Dict:
        return {
            "user_id": bot_Message_json.get("sender", {}).get("user_id", 0),
            "user_nickname": bot_Message_json.get("sender", {}).get("nickname", "未知"),
        }

    def get_common_message_info() -> Dict:
        return {
            "message": bot_Message_json.get("raw_message", ""),
            "message_id": bot_Message_json.get("message_id", -114514),
            "message_time": bot_Message_json.get("time", 11451459200),
            "raw": bot_Message_json.get("message", {}),
        }

    async def get_group_details(group_id: int) -> Dict:
        ws_recv = await Api.get_group_info(group_id)
        return ws_recv.get("data", {})

    Message_json = {"post_type": "消息"}
    Message_MessageType = bot_Message_json.get("message_type", "none")

    if Message_MessageType == "private":
        Message_json["message_type"] = "好友"
        Message_json["message"] = get_common_message_info()
        Message_json["sender"] = get_sender_info()

    elif Message_MessageType == "group":
        Message_json["message_type"] = "群聊"
        Message_Sender_User_role = bot_Message_json.get("sender", {}).get("role", "群员")

        translation_dict = {
            "owner": "群主",
            "admin": "管理",
            "member": "群员",
        }

        ws_recv_data = await get_group_details(bot_Message_json.get("group_id", 0))

        Message_json["group"] = {
            "group_id": bot_Message_json.get("group_id", 0),
            "group_name": ws_recv_data.get("group_name", ""),
            "group_member_count": ws_recv_data.get("member_count", 0),
            "group_max_member_count": ws_recv_data.get("max_member_count", 0),
        }
        Message_json["message"] = get_common_message_info()
        Message_json["sender"] = {
            **get_sender_info(),
            "user_role": translation_dict.get(Message_Sender_User_role, "群员"),
            "user_card": bot_Message_json.get("sender", {}).get("card", ""),
        }

    else:
        return bot_Message_json

    return Message_json
