import asyncio
import json
import os
import httpx
from utils.Manager.Config_Manager import connect_config_load
from utils.Manager.Log_Manager import Log
from Global.Global import GlobalVal

logger = Log()

class APIWrapper:
    def __init__(self):
        if os.path.exists("config/Bot/connect.json"):
            self.connect_config = connect_config_load()

    async def get(self, endpoint: str, **params):
        async with httpx.AsyncClient() as client:
            url = f'http://{self.connect_config["perpetua"]["host"]}:{self.connect_config["perpetua"]["http_api_port"]}{endpoint}'
            try:

                response = await client.post(url, json=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"无法调用 HTTP API：{e}")
                return None
            except httpx.RequestError as e:
                print(f"无法发起请求：{e}")
                return None


    async def delete_msg(self, Message_ID: int) -> dict:
        """
        撤回消息 API。

        参数:
            Message_ID (int): 消息 ID。

        返回:
            dict: 群信息的 JSON 数据。
        """
        if "perpetua" in self.connect_config:
            ws_recv = await (self.get(endpoint="/delete_msg", message_id = Message_ID))
            ws_recv_data = ws_recv.get("data", {})
            return ws_recv_data
        else:
            return "这个API暂未支持"
    async def set_friend_add_request(self, flag: str, approve: bool, remark: str = None) -> dict:
        """
        处理好友请求。

        参数:
            flag (str): 加好友请求的 flag。
            approve (bool): 操作类型： True为同意 相反 False为拒绝
            remark (str): 备注，非必须

        返回:
            dict: 无。
        """
        if "perpetua" in self.connect_config:
            ws_recv = await (self.get(endpoint="/set_friend_add_request", flag = flag, approve = approve, remark = remark))
            ws_recv_data = ws_recv.get("data", {})
            return ws_recv_data
        else:
            return "这个API暂未支持"
        
    async def set_group_add_request(self, flag: str, type: str , approve: bool, reason: str = None) -> dict:
        """
        处理群聊请求。

        参数:
            flag (str): 加群请求的 flag。
            type (str): 操作类型： add 或 invite, 请求类型（需与日志消息中的 sub_type 字段相符）
            approve (bool): 操作类型：True为同意 相反 False为拒绝
            reason (str): 拒绝理由: 仅在拒绝的时候可用

        返回:
            dict: 无。
        """
        if "perpetua" in self.connect_config:
            ws_recv = await (self.get(endpoint="/set_friend_add_request", flag = flag, type = type, approve = approve, reason = reason))
            ws_recv_data = ws_recv.get("data", {})
            return ws_recv_data
        else:
            return "这个API暂未支持"
        
    async def get_group_info(self, Group_ID: int) -> dict:
        """
        获取群信息的 API。

        参数:
            Group_ID (int): 群组 ID。

        返回:
            dict: 群信息的 JSON 数据。
        """
        if "perpetua" in self.connect_config:
            ws_recv = await (self.get(endpoint="/get_group_info", group_id = Group_ID, no_cache = False))
            ws_recv_data = ws_recv.get("data", {})
            return ws_recv_data
        else:
            return "这个API暂未支持"

    async def send_Groupmessage(
        self, Group_ID: int, Message_ID: int, Message: str, reply: bool = False
    ) -> str:
        """
        发送群消息的 API。

        参数:
            Group_ID (int): 群组 ID。
            Message_ID (int): 消息 ID。
            Message (str): 消息内容。
            reply (bool): 是否回复。

        返回:
            dict: 发送结果的 JSON 数据。
        """
        if "perpetua" in self.connect_config:
            
            if reply:
                Message = f"[CQ:reply,id={Message_ID}]{Message}"

            ws_recv = await (self.get(endpoint="/send_group_msg", group_id = Group_ID, message = Message))
            ws_recv_data = ws_recv.get("data", {})
            message_id = ws_recv_data.get("message_id", 0)
            ws_recv2 = await self.get_group_info(Group_ID)
            Group_Name = ws_recv2["group_name"]

            
            Message = Message.replace("\n", "\\n")

            log_message = f"[消息][群聊] {Message}  --To    {Group_Name}({Group_ID}) ({message_id})"

            logger.info(message=log_message,flag="Api",)
            return message_id


Api = APIWrapper()
