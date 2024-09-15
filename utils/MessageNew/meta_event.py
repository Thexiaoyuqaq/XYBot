from typing import Dict


async def format_meta_event(bot_Message_json: Dict) -> Dict:
    meta_event_json = bot_Message_json
    meta_event_json["post_type"] = "心跳包"
    return meta_event_json
