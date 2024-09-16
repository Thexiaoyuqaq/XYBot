from typing import Dict


async def format_notice(bot_Message_json: Dict) -> Dict:
    """
    格式化处理通知事件的函数。

    根据传入的 bot_Message_json 字典，格式化并返回一个标准化的通知事件字典。
    函数根据不同的 notice_type 处理不同类型的事件，并提供详细的信息。

    参数:
    bot_Message_json (Dict): 从机器人获取的原始事件数据字典。

    返回:
    Dict: 标准化的事件数据字典，包含可读事件名称。
    """

    # 定义通知类型与事件名称的映射字典
    notice_type_mapping = {
        "group_upload": "群文件上传",
        "group_admin": {
            "set": "管理员设置",
            "unset": "管理员取消"
        },
        "group_decrease": {
            "leave": "群成员减少",
            "kick": "群成员被踢出",
            "kick_me": "被踢出群聊"
        },
        "group_increase": {
            "approve": "群成员增加",
            "invite": "群成员邀请入群"
        },
        "group_ban": {
            "ban": "群成员被禁言",
            "lift_ban": "群成员解除禁言"
        },
        "group_recall": "群消息撤回",
        "friend_recall": "好友消息撤回",
        "notify": {
            "poke": "戳一戳",
            "honor": "群荣誉变更"
        }
    }

    def get_event_info() -> Dict:
        """
        根据 notice_type 从 bot_Message_json 中提取和格式化事件信息。

        返回:
        Dict: 事件信息字典，包含各种通知类型的具体数据。
        """
        # 从 bot_Message_json 中提取 notice_type
        notice_type = bot_Message_json.get("notice_type", "未知")

        # 基础的事件信息
        event_info = {
            "user_id": bot_Message_json.get("user_id", 0),
            "operator_id": bot_Message_json.get("operator_id", 0),
            "time": bot_Message_json.get("time", 0),  # 事件发生的时间戳，数字类型
            "group_id": bot_Message_json.get("group_id", 0),
        }

        # 根据不同的 notice_type 更新 event_info
        if notice_type == "group_upload":
            event_info.update(
                {
                    "file": {
                        "id": bot_Message_json.get("file", {}).get("id", ""),
                        "name": bot_Message_json.get("file", {}).get("name", ""),
                        "size": bot_Message_json.get("file", {}).get("size", 0),
                        "busid": bot_Message_json.get("file", {}).get("busid", 0),
                    }
                }
            )
        elif notice_type == "group_admin":
            event_info.update({"sub_type": bot_Message_json.get("sub_type", "未知")})
        elif notice_type == "group_decrease":
            event_info.update(
                {
                    "sub_type": bot_Message_json.get("sub_type", "未知"),
                    "operator_id": bot_Message_json.get("operator_id", 0),
                    "user_id": bot_Message_json.get("user_id", 0),
                }
            )
        elif notice_type == "group_increase":
            event_info.update(
                {
                    "sub_type": bot_Message_json.get("sub_type", "未知"),
                    "operator_id": bot_Message_json.get("operator_id", 0),
                    "user_id": bot_Message_json.get("user_id", 0),
                }
            )
        elif notice_type == "group_ban":
            event_info.update(
                {
                    "sub_type": bot_Message_json.get("sub_type", "未知"),
                    "user_id": bot_Message_json.get("user_id", 0),
                    "duration": bot_Message_json.get("duration", 0),
                }
            )
        elif notice_type == "group_recall":
            event_info.update({"message_id": bot_Message_json.get("message_id", 0)})
        elif notice_type == "friend_recall":
            event_info.update({"message_id": bot_Message_json.get("message_id", 0)})
        elif notice_type == "notify":
            if bot_Message_json.get("sub_type", "未知") == "poke":
                event_info.update(
                    {
                        "sub_type": bot_Message_json.get("sub_type", "未知"),  # 类型
                        "action_text": bot_Message_json.get(
                            "action", "戳了戳"
                        ),  # 戳一戳的文字
                        "action_suffix": bot_Message_json.get(
                            "suffix", ""
                        ),  # 戳一戳的附加文字
                        "user_id": bot_Message_json.get("user_id", 0),  # 戳的用户
                        "target_id": bot_Message_json.get("target_id", 0),  # 被戳用户
                        "group_id": bot_Message_json.get("group_id", 0),  # 事件群号
                        "time": bot_Message_json.get(
                            "time", 0
                        ),  # 事件发生的时间戳，数字类型
                    }
                )
            elif bot_Message_json.get("sub_type", "未知") == "honor":
                event_info.update(
                    {
                        "sub_type": bot_Message_json.get("sub_type", "未知"),
                        "target_id": bot_Message_json.get(
                            "target_id", 0
                        ),  # 适用于特定类型的 notify
                        "honor_type": bot_Message_json.get(
                            "honor_type", ""
                        ),  # 适用于荣誉类型的 notify
                    }
                )

        return event_info

    # 获取事件名称，替换事件类型为更具可读性的名字
    notice_type = bot_Message_json.get("notice_type", "未知")
    sub_type = bot_Message_json.get("sub_type", "未知")

    event_name = notice_type_mapping.get(notice_type, "未知")
    if isinstance(event_name, dict):
        event_name = event_name.get(sub_type, event_name.get("未知", "未知"))

    return {
        "post_type": "事件",  # 上报类型
        "notice_type": event_name,  # 通知类型替换为可读名称
        "event": get_event_info(),  # 事件信息
    }
