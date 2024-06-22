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

    async def async_request_post(self, endpoint, **params):
        async with httpx.AsyncClient() as client:
            try:
                url = f"http://{self.connect_config['perpetua']['host']}:{self.connect_config['perpetua']['http_api_port']}{endpoint}"
                response = await client.post(url= url, json=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"无法调用 HTTP API：{e}")
                return None
            except httpx.RequestError as e:
                print(f"出现错误: 无法调用{endpoint}端点：{e} \ndebug: url({url}) \n params({params}) \n请检查api端口是否畅通，并检查代理服务器是否关闭，如都不能解决请在github反馈")
                return None
            
    async def post(self, endpoint: str, **params):
        return await self.async_request_post(endpoint, **params)  


    async def delete_msg(self, Message_ID: int) -> dict:
        if "perpetua" in self.connect_config:
            return await self.post(endpoint="/delete_msg", message_id=Message_ID)
        else:
            return "这个API暂未支持"

    async def set_friend_add_request(self, flag: str, approve: bool, remark: str = None) -> dict:
        if "perpetua" in self.connect_config:
            return await self.post(endpoint="/set_friend_add_request", flag=flag, approve=approve, remark=remark)
        else:
            return "这个API暂未支持"

    async def set_group_add_request(self, flag: str, type: str, approve: bool, reason: str = None) -> dict:
        if "perpetua" in self.connect_config:
            return await self.post(endpoint="/set_group_add_request", flag=flag, type=type, approve=approve, reason=reason)
        else:
            return "这个API暂未支持"

    async def get_group_info(self, Group_ID: int) -> dict:
        if "perpetua" in self.connect_config:
            return await self.post(endpoint="/get_group_info", group_id=Group_ID, no_cache=False)
        else:
            return "这个API暂未支持"
    async def get_stranger_info(self, User_ID: int) -> dict:
        if "perpetua" in self.connect_config:
            return await self.post(endpoint="/get_stranger_info", user_id=User_ID)
        else:
            return "这个API暂未支持"

    async def send_Groupmessage(
            self, Group_ID: int, Message_ID: int, Message: str, reply: bool = False) -> str:
        if "perpetua" in self.connect_config:
            if reply:
                Message = f"[CQ:reply,id={Message_ID}]{Message}"

            ws_recv = await self.post(endpoint="/send_group_msg", group_id=Group_ID, message=Message)
            ws_recv_data = ws_recv.get("data", {})
            message_id = ws_recv_data.get("message_id", 0)
            ws_recv2 = await self.get_group_info(Group_ID)
            ws_recv2_data = ws_recv2.get("data", {})
            Group_Name = ws_recv2_data.get("group_name", "null")

            Message = Message.replace("\n", "\\n")

            log_message = f"[消息][群聊] {Message}  --To    {Group_Name}({Group_ID})   ({message_id})"

            logger.info(message=log_message, flag="Api")
            return message_id
    async def send_PrivateMessage(
            self, User_ID: int, Message_ID: int, Message: str, reply: bool = False
    ) -> str:
        if "perpetua" in self.connect_config:
            if reply:
                Message = f"[CQ:reply,id={Message_ID}]{Message}"

            ws_recv = await self.post(endpoint="/send_private_msg", user_id=User_ID, message=Message)
            ws_recv_data = ws_recv.get("data", {})
            message_id = ws_recv_data.get("message_id", 0)

            ws_recv2 = await self.get_stranger_info(User_ID)
            ws_recv2_data = ws_recv2.get("data", {})
            User_Name = ws_recv2_data.get("nickname", "null")

            Message = Message.replace("\n", "\\n")
            
            log_message = f"[消息][私聊] {Message}  --To    {User_Name}({User_ID})   ({message_id})"
            logger.info(message=log_message, flag="Api")
            return message_id


Api = APIWrapper()
