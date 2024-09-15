from typing import Dict

async def format_group_request(bot_Message_json: Dict) -> Dict:
    sub_type_translation_dict = {
        "add": "添加",
        "invite": "邀请",
    }

    group_request_json = {
        "post_type": "请求",
        "request_type": "群聊请求",
        "request": {
            "group_id": bot_Message_json.get("group_id", 0),
            "sub_type": sub_type_translation_dict.get(bot_Message_json.get("sub_type", "未知"), "未知"),
            "user_id": bot_Message_json.get("user_id", 0),
            "comment": bot_Message_json.get("comment", ""),
            "flag": bot_Message_json.get("flag", ""),
            "time": bot_Message_json.get("time", 11451459200),
        }
    }
    return group_request_json

async def format_friend_request(bot_Message_json: Dict) -> Dict:
    friend_request_json = {
        "post_type": "请求",
        "request_type": "好友请求",
        "request": {
            "user_id": bot_Message_json.get("user_id", 0),
            "comment": bot_Message_json.get("comment", ""),
            "flag": bot_Message_json.get("flag", ""),
            "time": bot_Message_json.get("time", 11451459200),
        }
    }
    return friend_request_json

async def format_request(bot_Message_json: Dict) -> Dict:
    request_type = bot_Message_json.get("request_type", "none")

    if request_type == "group":
        return format_group_request(bot_Message_json)
    elif request_type == "friend":
        return format_friend_request(bot_Message_json)
    else:
        return bot_Message_json
