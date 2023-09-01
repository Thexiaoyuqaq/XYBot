import html
import json
import re
import aiohttp
from utils.Manager.Config_Manager import *
from utils.Manager.Log_Manager import Log
logger = Log()

config_create()
config = config_load()
connect_config = connect_config_load()
class APIWrapper:
    def __init__(self):
        if "gocq" in connect_config:
            self.host = connect_config["gocq"]["cq_host"]
            self.http_port = connect_config["gocq"]["cq_http_port"]
        else:
            pass

    async def get_group_info(self,Group_ID: int) -> dict:
        """
        获取群信息的 API。
    
        参数:
            Group_ID (int): 群组 ID。
    
        返回:
            dict: 群信息的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/get_group_info?group_id={Group_ID}&no_cache=true"
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"
    async def get_forward_msg(self,Message_ID: int) -> dict:
        """
        获取合并消息 API。
    
        参数:
            Message_ID (int): 消息 ID。
    
        返回:
            dict: 合并消息的内容json。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/get_forward_msg?message_id={Message_ID}"
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"
    async def set_group_card(self,Group_ID: int, card: str, user_id: int) -> dict:
        """
        设置群员名片的 API。
        
        参数:
            Group_ID (int): 群组 ID。
            card (str): 群员名片。
            user_id (int): 群员 QQ 号。
    
        返回:
            dict: 设置结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/set_group_card?group_id={Group_ID}&user_id={user_id}&card={card}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"


    async def set_group_ban(self,Group_ID: int, user_id: int, time: int) -> dict:
        """
        设置群员禁言的 API。
        
        参数:
            Group_ID (int): 群组 ID。
            user_id (int): 群员 QQ 号。
            time (int): 禁言时间（单位：秒）。
    
        返回:
            dict: 设置结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/set_group_ban?group_id={Group_ID}&user_id={user_id}&duration={time}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"


    async def get_group_member_info(self,Group_ID: int, user_id: str) -> dict:
        """
        获取群成员信息的 API。
        
        参数:
            user_id: (int) 群员 QQ 号。
            Group_ID (int): 群组 ID。
    
        返回:
            dict: 群成员信息的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/get_group_member_info?group_id={Group_ID}&user_id={user_id}&no_cache=true"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"


    async def send_Groupmessage(self,Group_ID: int, Message_ID: int, Message: str, awa: bool) -> str:
        """
        发送群消息的 API。
    
        参数:
            Group_ID (int): 群组 ID。
            Message_ID (int): 消息 ID。
            Message (str): 消息内容。
            awa (bool): 是否回复。
    
        返回:
            dict: 发送结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/send_group_msg"
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
                            Group_Name = (await Api.get_group_info(Group_ID))["data"]["group_name"]
                            message_id = Requests["data"]["message_id"]
                            logger.info(message=f"[消息][群聊] {Message} --To {Group_Name}({Group_ID}) ({message_id})", flag="Api")
                            return Requests
                        else:
                            Group_Name = (await Api.get_group_info(Group_ID))["data"]["group_name"]
                            logger.warning(message=f"[消息][群聊] {Message} --To {Group_Name}({Group_ID})  --无法发送", flag="Api")
                            return "Error: 无法发送"
                    except json.JSONDecodeError:
                        logger.error(message="Invalid JSON response", flag="Api")
                        return "Error: 无效的 JSON 响应"

    async def send_FriendMessage(self,user_id: int, message: str) -> dict:
        """
        发送好友消息的 API。
        
        参数:
            user_id (int): QQ号。
            message (str): 消息内容。
    
        返回:
            dict: 发送结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/send_private_msg"
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
        else:
            return "这个API暂未支持"



    async def set_GroupRequest(self,flag: int, operate: bool) -> dict:
        """
        同意加群操作的 API。
        
        参数:
            flag (str): 请求标识。
            operate (bool): 操作。
        
        返回:
            dict: 操作结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/set_group_add_request?approve=true&type={operate}&flag={flag}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"


    async def set_FreindRequest(self,flag: int, operate: bool) -> dict:
        """
        同意好友操作的 API。
        
        参数:
            flag (str): 请求标识。
            operate (bool): 操作。
    
        返回:
            dict: 操作结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/set_friend_add_request?approve={operate}&flag={flag}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"


    async def delete_msg(self,message_id: int) -> dict:
        """
        撤回消息的 API。
        
        参数:
            message_id (int): 消息 ID。
        
        返回:
            dict: 操作结果的 JSON 数据。
        """
        if "gocq" in connect_config:
            url = f"http://{self.host}:{self.http_port}/delete_msg?message_id={message_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Requests = await response.json()
                    return Requests
        else:
            return "这个API暂未支持"
Api = APIWrapper()