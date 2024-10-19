import asyncio
import json
import os
import httpx
from utils.Manager.Config_Manager import connect_config_load
from utils.Manager.Log_Manager import Log

logger = Log()

class APIWrapper:
    def __init__(self):
        """
        初始化API封装器，加载配置文件。
        """
        self.connect_config = self.load_config()

    def load_config(self):
        """
        加载连接配置文件。
        """
        config_path = "config/Bot/connect.json"
        if os.path.exists(config_path):
            return connect_config_load()
        logger.warning("未找到配置文件，请检查配置路径。")
        return None

    async def async_request_post(self, endpoint, **params):
        """
        发送POST请求，处理HTTP和网络错误。
        """
        if not self.connect_config:
            return {"error": "API未配置"}

        url = (
            f"http://{self.connect_config['perpetua']['host']}:"
            f"{self.connect_config['perpetua']['http_api_port']}{endpoint}"
        )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url=url, json=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP错误: {e.response.status_code} {e.response.text}")
                return None
            except httpx.RequestError as e:
                logger.error(
                    f"请求错误：调用 {endpoint} 时出现问题。\n"
                    f"URL: {url}\n参数: {params}\n错误: {str(e)}"
                )
                return None

    async def post(self, endpoint: str, **params):
        """
        封装POST请求，提供调用接口。
        """
        return await self.async_request_post(endpoint, **params)

    async def api_request(self, endpoint: str, **params):
        """
        统一处理API调用逻辑，避免冗余。
        """
        if "perpetua" not in self.connect_config:
            return {"error": "该API暂未支持"}
        return await self.post(endpoint, **params)

    async def send_message(self, endpoint: str, target_id: int, message: str, reply_id=None):
        """
        发送消息的通用方法，用于群聊和私聊。
        """
        if reply_id:
            message = f"[CQ:reply,id={reply_id}]{message}"

        ws_recv = await self.api_request(endpoint=endpoint, group_id=target_id, message=message)
        message_id = ws_recv.get("data", {}).get("message_id", 0)
        return message_id

    async def send_group_message(self, group_id: int, message: str, reply_id=None):
        """
        发送群聊消息。
        """
        message_id = await self.send_message("/send_group_msg", group_id, message, reply_id)
        group_info = await self.get_group_info(group_id)
        group_name = group_info.get("data", {}).get("group_name", "null")

        log_message = f"[消息][群聊] {message} --To {group_name}({group_id}) ({message_id})"
        logger.info(log_message, flag="Api")
        return message_id

    async def send_private_message(self, user_id: int, message: str, reply_id=None):
        """
        发送私聊消息。
        """
        message_id = await self.send_message("/send_private_msg", user_id, message, reply_id)
        user_info = await self.get_stranger_info(user_id)
        user_name = user_info.get("data", {}).get("nickname", "null")

        log_message = f"[消息][私聊] {message} --To {user_name}({user_id}) ({message_id})"
        logger.info(log_message, flag="Api")
        return message_id

    async def get_group_info(self, group_id: int):
        """
        获取群信息。
        """
        return await self.api_request("/get_group_info", group_id=group_id, no_cache=True)

    async def get_stranger_info(self, user_id: int):
        """
        获取陌生人信息。
        """
        return await self.api_request("/get_stranger_info", user_id=user_id)

    async def delete_msg(self, message_id: int):
        """
        撤回消息。
        """
        return await self.api_request("/delete_msg", message_id=message_id)

    async def set_friend_add_request(self, flag: str, approve: bool, remark=None):
        """
        处理好友添加请求。
        """
        return await self.api_request(
            "/set_friend_add_request", flag=flag, approve=approve, remark=remark
        )

    async def set_group_add_request(self, flag: str, request_type: str, approve: bool, reason=None):
        """
        处理加群请求。
        """
        return await self.api_request(
            "/set_group_add_request", flag=flag, type=request_type, approve=approve, reason=reason
        )

    async def set_group_card(self, group_id: int, user_id: int, card=""):
        """
        设置群名片。
        """
        return await self.api_request("/set_group_card", group_id=group_id, user_id=user_id, card=card)

    async def send_group_forward_msg(self, group_id: int, messages: str):
        """
        发送群合并消息。
        """
        return await self.api_request("/send_group_forward_msg", group_id=group_id, messages=messages)

    async def send_private_forward_msg(self, user_id: int, messages: str):
        """
        发送私聊合并消息。
        """
        return await self.api_request("/send_private_forward_msg", group_id=user_id, messages=messages)


# 实例化 APIWrapper
Api = APIWrapper()
