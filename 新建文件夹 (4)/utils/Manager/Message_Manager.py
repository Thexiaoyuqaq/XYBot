from utils.Api.Command_Api import Api

async def Message_to_New(bot_Message_json: dict):
    Message_json = {}

    Message_PostType = bot_Message_json.get("post_type", "none")

    def get_sender_info():
        return {
            "user_id": bot_Message_json.get("sender", {}).get("user_id", 0),
            "user_nickname": bot_Message_json.get("sender", {}).get("nickname", "未知"),
        }

    def get_group_info(ws_recv_data):
        return {
            "group_id": bot_Message_json.get("group_id", 0),
            "group_name": ws_recv_data.get("group_name", ""),
            "group_member_count": ws_recv_data.get("member_count", 0),
            "group_max_member_count": ws_recv_data.get("max_member_count", 0),
        }

    def get_common_message_info():
        return {
            "message": bot_Message_json.get("raw_message", ""),
            "message_id": bot_Message_json.get("message_id", -114514),
            "message_time": bot_Message_json.get("time", 11451459200),
            "raw": bot_Message_json.get("message", {}),
        }

    async def get_group_details(group_id):
        ws_recv = await Api.get_group_info(group_id)
        return ws_recv.get("data", {})

    if Message_PostType == "message":
        Message_json["post_type"] = "消息"
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

            Message_json["group"] = get_group_info(ws_recv_data)
            Message_json["message"] = get_common_message_info()
            Message_json["sender"] = {
                **get_sender_info(),
                "user_role": translation_dict.get(Message_Sender_User_role, "群员"),
                "user_card": bot_Message_json.get("sender", {}).get("card", ""),
            }

    elif Message_PostType == "meta_event":
        Message_json = bot_Message_json
        Message_json["post_type"] = "心跳包"

    elif Message_PostType == "notice":
        Message_json["post_type"] = "事件"
        Message_NoticeType = bot_Message_json.get("notice_type", "未知")

        notice_translation_dict = {
            "group_increase": "群成员增加",
            "group_decrease": "群成员减少",
            "group_recall": "群消息撤回",
            "friend_recall": "好友消息撤回",
            "group_ban": "群禁言",
            "poke": "戳一戳",
        }

        sub_type_translation_dict = {
            "approve": "主动",
            "invite": "邀请",
            "leave": "主动",
            "kick": "踢出",
            "kick_me": "被踢",
            "ban": "禁言",
            "lift_ban": "解除禁言",
        }

        Message_json["notice_type"] = notice_translation_dict.get(Message_NoticeType, "未知")

        if Message_NoticeType in {"group_increase", "group_decrease", "group_recall", "friend_recall", "group_ban", "poke"}:
            event_info = {
                "user_id": bot_Message_json.get("user_id", 0),
                "operator_id": bot_Message_json.get("operator_id", 0),
                "time": bot_Message_json.get("time", "123456"),
                "group_id": bot_Message_json.get("group_id", 0),
            }
            if Message_NoticeType == "group_increase":
                event_info.update({
                    "sub_type": sub_type_translation_dict.get(bot_Message_json.get("sub_type", "未知"), "未知"),
                })
            elif Message_NoticeType == "group_decrease":
                event_info.update({
                    "sub_type": sub_type_translation_dict.get(bot_Message_json.get("sub_type", "未知"), "未知"),
                })
            elif Message_NoticeType == "group_recall":
                event_info.update({
                    "message_id": bot_Message_json.get("message_id", 0),
                })
            elif Message_NoticeType == "friend_recall":
                event_info.update({
                    "message_id": bot_Message_json.get("message_id", 0),
                })
            elif Message_NoticeType == "group_ban":
                event_info.update({
                    "duration": bot_Message_json.get("duration", 0),
                    "sub_type": sub_type_translation_dict.get(bot_Message_json.get("sub_type", "未知"), "未知"),
                })
            elif Message_NoticeType == "poke":
                event_info.update({
                    "target_id": bot_Message_json.get("target_id", 0),
                })
            Message_json["event"] = event_info

    elif Message_PostType == "request":
        Message_json["post_type"] = "请求"
        Message_RequestType = bot_Message_json.get("request_type", "none")

        sub_type_translation_dict = {
            "add": "添加",
            "invite": "邀请",
        }

        if Message_RequestType == "group":
            Message_json["request_type"] = "群聊请求"
            Message_json["request"] = {
                "group_id": bot_Message_json.get("group_id", 0),
                "sub_type": sub_type_translation_dict.get(bot_Message_json.get("sub_type", "未知"), "未知"),
                "user_id": bot_Message_json.get("user_id", 0),
                "comment": bot_Message_json.get("comment", ""),
                "flag": bot_Message_json.get("flag", ""),
                "time": bot_Message_json.get("time", 11451459200),
            }

    else:
        return bot_Message_json

    return Message_json
