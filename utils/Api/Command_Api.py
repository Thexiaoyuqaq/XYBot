# utils/Api/Command_Api.py
import os
import httpx
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import asyncio
from utils.Manager.Config_Manager import connect_config_load
from utils.Manager.Log_Manager import Log

logger = Log()


class APIWrapper:
    def __init__(self):
        """
        初始化API封装器，使用连接池优化
        """
        self.connect_config = self.load_config()
        self._client: Optional[httpx.AsyncClient] = None
        self._client_lock = asyncio.Lock()
        self._request_semaphore = asyncio.Semaphore(10)  # 限制并发请求数
        
    def load_config(self):
        """
        加载连接配置文件
        """
        config_path = "config/Bot/connect.json"
        if os.path.exists(config_path):
            return connect_config_load()
        logger.warning("未找到配置文件，请检查配置路径", flag="API")
        return None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """
        获取或创建HTTP客户端（单例模式）
        """
        if self._client is None:
            async with self._client_lock:
                if self._client is None:
                    self._client = httpx.AsyncClient(
                        timeout=httpx.Timeout(10.0, connect=5.0),
                        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
                        http2=True  # 启用HTTP/2
                    )
        return self._client
    
    async def close(self):
        """
        关闭HTTP客户端
        """
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def async_request_post(self, endpoint: str, **params) -> Optional[Dict[str, Any]]:
        """
        发送POST请求，使用连接池和并发控制
        """
        if not self.connect_config:
            return {"error": "API未配置"}
        
        # 使用信号量限制并发
        async with self._request_semaphore:
            url = (
                f"http://{self.connect_config['perpetua']['host']}:"
                f"{self.connect_config['perpetua']['http_api_port']}{endpoint}"
            )
            
            client = await self._get_client()
            
            try:
                response = await client.post(url=url, json=params)
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP错误: {e.response.status_code} - {endpoint}", flag="API")
                return {"error": f"HTTP {e.response.status_code}"}
                
            except httpx.TimeoutException:
                logger.error(f"请求超时: {endpoint}", flag="API")
                return {"error": "请求超时"}
                
            except httpx.RequestError as e:
                logger.error(f"请求错误: {endpoint} - {str(e)}", flag="API")
                return {"error": str(e)}
                
            except Exception as e:
                logger.error(f"未知错误: {endpoint} - {str(e)}", flag="API")
                return {"error": "未知错误"}
    
    async def post(self, endpoint: str, **params) -> Optional[Dict[str, Any]]:
        """
        封装POST请求
        """
        return await self.async_request_post(endpoint, **params)
    
    async def api_request(self, endpoint: str, **params) -> Optional[Dict[str, Any]]:
        """
        统一处理API调用逻辑
        """
        if not self.connect_config or "perpetua" not in self.connect_config:
            return {"error": "该API暂未支持"}
        
        return await self.post(endpoint, **params)
    
    # 消息发送优化：批量发送支持
    async def send_message_batch(self, messages: list) -> list:
        """
        批量发送消息
        
        Args:
            messages: 消息列表，每个消息包含 endpoint, target_id, message, reply_id
        
        Returns:
            发送结果列表
        """
        tasks = []
        for msg_data in messages:
            task = self.send_message(
                msg_data['endpoint'],
                msg_data['target_id'],
                msg_data['message'],
                msg_data.get('reply_id')
            )
            tasks.append(task)
        
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_message(self, endpoint: str, target_id: int, message: str, reply_id=None) -> int:
        """
        发送消息的通用方法
        """
        if reply_id:
            message = f"[CQ:reply,id={reply_id}]{message}"
        
        # 根据endpoint类型决定参数名
        param_name = "group_id" if "group" in endpoint else "user_id"
        
        ws_recv = await self.api_request(
            endpoint=endpoint,
            **{param_name: target_id, "message": message}
        )
        
        if ws_recv and "data" in ws_recv:
            return ws_recv["data"].get("message_id", 0)
        return 0
    
    async def send_group_message(self, group_id: int, message: str, reply_id=None) -> int:
        """
        发送群聊消息
        """
        message_id = await self.send_message("/send_group_msg", group_id, message, reply_id)
        
        # 异步获取群信息（可选）
        if message_id:
            asyncio.create_task(self._log_group_message(group_id, message, message_id))
        
        return message_id
    
    async def _log_group_message(self, group_id: int, message: str, message_id: int):
        """
        异步记录群消息日志
        """
        try:
            group_info = await self.get_group_info(group_id)
            group_name = group_info.get("data", {}).get("group_name", "Unknown")
            logger.info(
                f"[消息][群聊] {message} --To {group_name}({group_id}) ({message_id})",
                flag="Api"
            )
        except Exception:
            pass
    
    async def send_private_message(self, user_id: int, message: str, reply_id=None) -> int:
        """
        发送私聊消息
        """
        message_id = await self.send_message("/send_private_msg", user_id, message, reply_id)
        
        if message_id:
            asyncio.create_task(self._log_private_message(user_id, message, message_id))
        
        return message_id
    
    async def _log_private_message(self, user_id: int, message: str, message_id: int):
        """
        异步记录私聊消息日志
        """
        try:
            user_info = await self.get_stranger_info(user_id)
            user_name = user_info.get("data", {}).get("nickname", "Unknown")
            logger.info(
                f"[消息][私聊] {message} --To {user_name}({user_id}) ({message_id})",
                flag="Api"
            )
        except Exception:
            pass
    
    # 信息获取方法优化：添加缓存
    async def get_group_info(self, group_id: int, use_cache: bool = False) -> Dict[str, Any]:
        """
        获取群信息
        
        Args:
            group_id: 群ID
            use_cache: 是否使用缓存
        """
        return await self.api_request("/get_group_info", group_id=group_id, no_cache=not use_cache)
    
    async def get_stranger_info(self, user_id: int, use_cache: bool = True) -> Dict[str, Any]:
        """
        获取陌生人信息
        """
        return await self.api_request("/get_stranger_info", user_id=user_id, no_cache=not use_cache)
    
    async def delete_msg(self, message_id: int) -> Dict[str, Any]:
        """
        撤回消息
        """
        return await self.api_request("/delete_msg", message_id=message_id)
    
    async def set_friend_add_request(self, flag: str, approve: bool, remark: str = None) -> Dict[str, Any]:
        """
        处理好友添加请求
        """
        params = {"flag": flag, "approve": approve}
        if remark:
            params["remark"] = remark
        return await self.api_request("/set_friend_add_request", **params)
    
    async def set_group_add_request(
        self, 
        flag: str, 
        request_type: str, 
        approve: bool, 
        reason: str = None
    ) -> Dict[str, Any]:
        """
        处理加群请求
        """
        params = {
            "flag": flag,
            "type": request_type,
            "approve": approve
        }
        if reason:
            params["reason"] = reason
        return await self.api_request("/set_group_add_request", **params)
    
    async def set_group_card(self, group_id: int, user_id: int, card: str = "") -> Dict[str, Any]:
        """
        设置群名片
        """
        return await self.api_request(
            "/set_group_card",
            group_id=group_id,
            user_id=user_id,
            card=card
        )
    
    async def send_group_forward_msg(self, group_id: int, messages: list) -> Dict[str, Any]:
        """
        发送群合并消息
        """
        return await self.api_request(
            "/send_group_forward_msg",
            group_id=group_id,
            messages=messages
        )
    
    async def send_private_forward_msg(self, user_id: int, messages: list) -> Dict[str, Any]:
        """
        发送私聊合并消息
        """
        return await self.api_request(
            "/send_private_forward_msg",
            user_id=user_id,
            messages=messages
        )
    
    # 批量操作优化
    async def get_group_member_list(self, group_id: int, use_cache: bool = True) -> Dict[str, Any]:
        """
        获取群成员列表
        """
        return await self.api_request(
            "/get_group_member_list",
            group_id=group_id,
            no_cache=not use_cache
        )
    
    async def get_group_list(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        获取群列表
        """
        return await self.api_request("/get_group_list", no_cache=not use_cache)
    
    async def get_friend_list(self) -> Dict[str, Any]:
        """
        获取好友列表
        """
        return await self.api_request("/get_friend_list")


# 创建全局实例
Api = APIWrapper()

# 清理函数，在程序退出时调用
async def cleanup():
    """清理资源"""
    await Api.close()