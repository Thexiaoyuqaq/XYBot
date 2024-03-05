import asyncio
import json
import os
from utils.Manager.Config_Manager import connect_config_load
from utils.Manager.Log_Manager import Log
from Global.Global import GlobalVal

logger = Log()

if os.path.exists("config/Bot/connect.json"):
    connect_config = connect_config_load()


class APIWrapper:

    async def get_group_info(self, Group_ID: int) -> dict:
        """
        获取群信息的 API。

        参数:
            Group_ID (int): 群组 ID。

        返回:
            dict: 群信息的 JSON 数据。
        """
        if "perpetua" in connect_config:
            async with GlobalVal.lock:
                await GlobalVal.websocket.send(
                    json.dumps(
                        {
                            "action": "get_group_info",
                            "params": {"group_id": Group_ID, "no_cache": False},
                        }
                    )
                )

                ws_recv = await GlobalVal.websocket.recv()
            ws_recv = json.loads(ws_recv)
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
        if "perpetua" in connect_config:
            if reply:
                Message = f"[CQ:reply,id={Message_ID}]{Message}"
            async with GlobalVal.lock:
                await GlobalVal.websocket.send(
                    json.dumps(
                        {
                            "action": "send_group_msg",
                            "params": {"group_id": Group_ID, "message": Message},
                        }
                    )
                )
                ws_recv = await GlobalVal.websocket.recv()
            ws_recv = json.loads(ws_recv)

            ws_recv_data = ws_recv.get("data", {})
            message_id = ws_recv_data.get("message_id", 0)

            ## 由于获取群信息过于耗时，暂注释 后续也许会解决
            # ws_recv2 = await self.get_group_info(Group_ID)
            # Group_Name = ws_recv2["group_name"]
            # logger.info(message=f"[消息][群聊] {Message} --To    {Group_Name}({Group_ID}) ({message_id})",flag="Api",)
            logger.info(
                message=f"[发送][群聊] {Group_ID}：  {Message}           ({message_id})",
                flag="Api",
            )
            return message_id


Api = APIWrapper()
