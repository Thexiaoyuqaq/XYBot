from typing import Dict

async def format_notice(bot_Message_json: Dict) -> Dict:
    # print(bot_Message_json)
    
    # 定义通知类型与事件名称的映射字典
    notice_type_mapping = {
        "group_upload": {
            "name": "群文件上传",
            "sub_type": {}
        },
        "group_admin": {
            "name": "群管理员变动",
            "sub_type": {
                "set": "管理员设置",
                "unset": "管理员取消"
            }
        },
        "group_decrease": {
            "name": "群成员减少",
            "sub_type": {
                "leave": "主动退群",
                "kick": "成员被踢出",
                "kick_me": "被踢出群聊"
            }
        },
        "group_increase": {
            "name": "群成员增加",
            "sub_type": {
                "approve": "管理员同意入群",
                "invite": "管理员邀请入群"
            }
        },
        "group_ban": {
            "name": "群禁言",
            "sub_type": {
                "ban": "禁言",
                "lift_ban": "解除禁言"
            }
        },
        "group_recall": {
            "name": "群消息撤回",
            "sub_type": {}
        },
        "friend_recall": {
            "name": "好友消息撤回",
            "sub_type": {}
        },
        "friend_add": {
            "name": "好友添加",
            "sub_type": {}
        },
        "notify": {
            "name": "通知",
            "sub_type": {
                "poke": "戳一戳",
                "honor": "群荣誉变更"
            }
        }
    }

    def get_event_info() -> Dict:
        notice_type = bot_Message_json.get("notice_type", "未知")
        event_info = {
            "user_id": bot_Message_json.get("user_id", 0),
            "operator_id": bot_Message_json.get("operator_id", 0),
            "time": bot_Message_json.get("time", 0),
            "group_id": bot_Message_json.get("group_id", 0),
        }

        if notice_type == "group_upload":
            event_info.update({
                "file": {
                    "id": bot_Message_json.get("file", {}).get("id", ""),
                    "name": bot_Message_json.get("file", {}).get("name", ""),
                    "size": bot_Message_json.get("file", {}).get("size", 0),
                    "busid": bot_Message_json.get("file", {}).get("busid", 0),
                }
            })
        elif notice_type in ["group_admin", "group_decrease", "group_increase", "group_ban"]:
            sub_type = bot_Message_json.get("sub_type", "未知")
            event_info.update({"sub_type": sub_type})

            if notice_type == "group_ban":
                event_info.update({
                    "duration": bot_Message_json.get("duration", 0),
                })
        elif notice_type in ["group_recall", "friend_recall"]:
            event_info.update({"message_id": bot_Message_json.get("message_id", 0)})
            event_info.update({"tip": bot_Message_json.get("tip", "")})
        elif notice_type == "notify":
            sub_type = bot_Message_json.get("sub_type", "未知")
            if sub_type == "poke":
                event_info.update(
                    {
                        "action_text": bot_Message_json.get("action", "戳了戳"),
                        "action_suffix": bot_Message_json.get("suffix", ""),
                        "target_id": bot_Message_json.get("target_id", 0),
                        "sub_type": "戳一戳"
                    }
                )
            elif sub_type == "honor":
                event_info.update(
                    {
                        "target_id": bot_Message_json.get("target_id", 0),
                        "honor_type": bot_Message_json.get("honor_type", ""),
                        "sub_type": "群荣誉变更"
                    }
                )

        return event_info

    # 获取事件名称
    notice_type = bot_Message_json.get("notice_type", "未知")
    event_name = notice_type_mapping.get(notice_type, {}).get("name", "未知")

    return {
        "post_type": "事件",
        "notice_type": event_name,  # 用可读名称替换原通知类型
        "event": get_event_info(),  # 事件信息
    }
