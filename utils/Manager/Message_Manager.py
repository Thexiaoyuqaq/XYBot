import asyncio
from typing import Dict
from utils.MessageNew import message, meta_event, notice, request

async def process_message(bot_Message_json: Dict) -> Dict:
    return await message.format_message(bot_Message_json)

async def process_meta_event(bot_Message_json: Dict) -> Dict:
    return await meta_event.format_meta_event(bot_Message_json)

async def process_notice(bot_Message_json: Dict) -> Dict:
    return await notice.format_notice(bot_Message_json)

async def process_request(bot_Message_json: Dict) -> Dict:
    return await request.format_request(bot_Message_json)

async def MessageNew(bot_Message_json: Dict) -> Dict:
    post_type = bot_Message_json.get("post_type")

    if post_type == "message":
        result = await process_message(bot_Message_json)
    elif post_type == "meta_event":
        result = await process_meta_event(bot_Message_json)
    elif post_type == "notice":
        result = await process_notice(bot_Message_json)
    elif post_type == "request":
        result = await process_request(bot_Message_json)
    else:
        result = {"post_type": post_type, **bot_Message_json}

    return result
