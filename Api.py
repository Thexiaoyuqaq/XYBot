import json
import re
import aiohttp
from config import *
from LogSys import Log
logger = Log()

config_create()
config = config_load()
connect_config = connect_config_load()

host = connect_config["gocq"]["cq_host"]
http_port = connect_config["gocq"]["cq_http_port"]

def extract_id(text: str) -> int:
    """
    从回复消息中提取消息id
    
    Args:
        text (str): 消息
    
    Returns:
        str: 提取到的ID。
    """
    match_object = re.search(r"\[CQ:reply,id=(-?\d+)", text)
    if match_object:
        reply_id = match_object.group(1)
        return(reply_id)
    else:
        return None


def cn_u(text: str) -> str:
    """
    将文本转换为 Unicode 编码。
    
    Args:
        text (str): 文本字符串。
    
    Returns:
        str: Unicode 编码后的字符串。
    """
    return text.encode('unicode_escape').decode()


async def get_group_info(Group_ID: int) -> dict:
    """
    获取群信息的 API。
    
    Args:
        Group_ID (int): 群组 ID。
    
    Returns:
        dict: 群信息的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/get_group_info?group_id={Group_ID}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests


async def set_group_card(Group_ID: int, card: str, user_id: int) -> dict:
    """
    设置群员名片的 API。
    
    Args:
        Group_ID (int): 群组 ID。
        card (str): 群员名片。
        user_id (int): 群员 QQ 号。
    
    Returns:
        dict: 设置结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_group_card?group_id={Group_ID}&user_id={user_id}&card={card}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests


async def set_group_ban(Group_ID: int, user_id: int, time: int) -> dict:
    """
    设置群员禁言的 API。
    
    Args:
        Group_ID (int): 群组 ID。
        user_id (int): 群员 QQ 号。
        time (int): 禁言时间（单位：秒）。
    
    Returns:
        dict: 设置结果的 JSON 数据。
    """
    if user_id != 3443135327:
        url = f"http://{host}:{http_port}/set_group_ban?group_id={Group_ID}&user_id={user_id}&duration={time}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                Requests = await response.json()
                return Requests


async def get_group_member_info(Group_ID: int, user_id: str) -> dict:
    """
    获取群成员信息的 API。
    
    Args:
        user_id: (int) 群员 QQ 号。
        Group_ID (int): 群组 ID。
    
    Returns:
        dict: 群成员信息的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/get_group_member_info?group_id={Group_ID}&user_id={user_id}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests


async def send_Groupmessage(Group_ID: int, Message_ID: int, Message: str, awa: bool) -> str:
    """
    发送群消息的 API。
    
    Args:
        Group_ID (int): 群组 ID。
        Message_ID (int): 消息 ID。
        Message (str): 消息内容。
        awa (bool): 是否回复。
    
    Returns:
        dict: 发送结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/send_group_msg"
    payload = {
        "group_id": Group_ID,
        "message": Message
    }
    if awa:
        payload["message"] = f"[CQ:reply,id={Message_ID}]{Message}"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            try:
                Requests = await response.json()
                event_send_message = Requests["message"]
                if event_send_message != -1:
                    Group_Name = (await get_group_info(Group_ID))["data"]["group_name"]
                    message_id = Requests["data"]["message_id"]
                    logger.info(message=f"[消息][群聊] {Message} --To {Group_Name}({Group_ID}) ({message_id})", flag="Api")
                    return Requests
                else:
                    Group_Name = (await get_group_info(Group_ID))["data"]["group_name"]
                    logger.warning(message=f"[消息][群聊] {Message} --To {Group_Name}({Group_ID})  --无法发送", flag="Api")
                    return "Error: 无法发送"
            except json.JSONDecodeError:
                logger.error(message="Invalid JSON response", flag="Api")
                return "Error: 无效的 JSON 响应"

async def send_FriendMessage(user_id: int, message: str) -> dict:
    """
    发送好友消息的 API。
    
    Args:
        user_id (int): QQ号。
        message (str): 消息内容。
    
    Returns:
        dict: 发送结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/send_private_msg"
    params = {
        "user_id": user_id,
        "message": message
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            try:
                Requests = await response.json()
                message_id = Requests["data"]["message_id"]
                logger.info(message=f"[消息][好友] {message} --To {user_id} ({message_id})", flag="Api")
                return Requests
            except aiohttp.ContentTypeError:
                logger.error(message="Invalid JSON response", flag="Api")
                return {"error": "Invalid JSON response"}



async def set_GroupRequest(flag: int, operate: bool) -> dict:
    """
    同意加群操作的 API。
    
    Args:
        flag (str): 请求标识。
        operate (bool): 操作。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_group_add_request?approve=true&type={operate}&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests


async def set_FreindRequest(flag: int, operate: bool) -> dict:
    """
    同意好友操作的 API。
    
    Args:
        flag (str): 请求标识。
        operate (bool): 操作。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_friend_add_request?approve={operate}&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests


async def delete_msg(message_id: int) -> dict:
    """
    撤回消息的 API。
    
    Args:
        message_id (int): 消息 ID。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/delete_msg?message_id={message_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            Requests = await response.json()
            return Requests
