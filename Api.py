import datetime
import re
import aiohttp
from config import get_config

host = get_config('gocq', 'host')
http_port = get_config('gocq', 'http_port')

def extract_id(text: str) -> str:
    """
    从文本中提取ID。
    
    Args:
        text (str): 文本字符串。
    
    Returns:
        str: 提取到的ID。
    """
    pattern = r"id=(-?\d+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def get_ban_time(text: str) -> str:
    """
    从文本中获取禁言时间。
    
    Args:
        text (str): 文本字符串。
    
    Returns:
        str: 禁言时间。
    """
    result = re.search(r'\b(\d+)\b$', text)
    if result:
        number = result.group(1)
        return number

def get_ban_id(text: str) -> str:
    """
    从文本中获取禁言的 QQ 号。
    
    Args:
        text (str): 文本字符串。
    
    Returns:
        str: QQ 号。
    """
    result = re.search(r'qq=(\d+)', text)
    if result:
        qq_number = result.group(1)
        return qq_number

def cn_u(text: str) -> str:
    """
    将文本转换为 Unicode 编码。
    
    Args:
        text (str): 文本字符串。
    
    Returns:
        str: Unicode 编码后的字符串。
    """
    return(text.encode('unicode_escape').decode())

async def get_group_info(event_message_Group_ID: str) -> dict:
    """
    获取群信息的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
    
    Returns:
        dict: 群信息的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/get_group_info?group_id={event_message_Group_ID}&no_cache=true" 
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def set_group_card(event_message_Group_ID: str, card: str, user_id: str) -> dict:
    """
    设置群员名片的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
        card (str): 群员名片。
        user_id (str): 群员 QQ 号。
    
    Returns:
        dict: 设置结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_group_card?group_id={event_message_Group_ID}&user_id={user_id}&card={card}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def set_group_ban(event_message_Group_ID: str, user_id: str, time: int) -> dict:
    """
    设置群员禁言的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
        user_id (str): 群员 QQ 号。
        time (int): 禁言时间（单位：秒）。
    
    Returns:
        dict: 设置结果的 JSON 数据。
    """
    if user_id != 3443135327:
        url = f"http://{host}:{http_port}/set_group_ban?group_id={event_message_Group_ID}&user_id={user_id}&duration={time}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rsjson = await response.json()
                return rsjson

async def get_group_member_info(event_message_Group_ID: str, userid: str) -> dict:
    """
    获取群成员信息的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
        userid (str): 群员 QQ 号。
    
    Returns:
        dict: 群成员信息的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/get_group_member_info?group_id={event_message_Group_ID}&user_id={userid}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def send_group_forward_msg(event_message_Group_ID: str, event_message_Message: str) -> dict:
    """
    发送合并消息的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
        event_message_Message (str): 消息内容。
    
    Returns:
        dict: 发送结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/send_group_forward_msg?group_id={event_message_Group_ID}&messages={event_message_Message}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def send_Groupmessage(event_message_Group_ID: str, event_message_Message_ID: str, event_message_Message: str, awa: bool) -> dict:
    """
    发送群消息的 API。
    
    Args:
        event_message_Group_ID (str): 群组 ID。
        event_message_Message_ID (str): 消息 ID。
        event_message_Message (str): 消息内容。
        awa (bool): 是否自动回复。
    
    Returns:
        dict: 发送结果的 JSON 数据。
    """
    if awa:
        url = f"http://{host}:{http_port}/send_group_msg?group_id={event_message_Group_ID}&message=[CQ:reply,id=" + str(event_message_Message_ID) + "]" + event_message_Message
    else:
        url = f"http://{host}:{http_port}/send_group_msg?group_id={event_message_Group_ID}&message={event_message_Message}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            event_send_message = rsjson["message"]
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            
            if event_send_message != -1:
                event_message_Group_Name = await get_group_info(event_message_Group_ID)
                event_message_Group_Name = event_message_Group_Name["data"]["group_name"]
                print("[" + str(time_str) + "][INFO][Message][Send][Group] {} --To {}({})   ({})".format(event_message_Message, event_message_Group_Name, event_message_Group_ID, rsjson["data"]["message_id"]))
                return rsjson
            else:
                print("[" + str(time_str) + "][INFO][Message][Send][Group] {} --To {}".format(event_message_Message, event_message_Group_ID))
                return "Error: 无法发送"

async def set_GroupRequest(flag: str, type: str) -> dict:
    """
    同意加群操作的 API。
    
    Args:
        flag (str): 请求标识。
        type (str): 请求类型。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_group_add_request?approve=true&type={type}&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def set_FreindRequest(flag: str) -> dict:
    """
    同意好友操作的 API。
    
    Args:
        flag (str): 请求标识。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/set_friend_add_request?approve=true&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson

async def delete_msg(message_id: str) -> dict:
    """
    撤回消息的 API。
    
    Args:
        message_id (str): 消息 ID。
    
    Returns:
        dict: 操作结果的 JSON 数据。
    """
    url = f"http://{host}:{http_port}/delete_msg?message_id={message_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
