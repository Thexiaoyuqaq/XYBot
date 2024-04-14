import os
import json
import asyncio
import websockets
from utils.Manager.Config_Manager import config_create, config_load, connect_config_load
from utils.Api.Plugin_Api import Plugin_Api
from utils.Api.Bot_Api import Bot
from utils.Manager.Plugin_Manager import load_plugins
from utils.Manager.Log_Manager import Log
from Log import cmd_Log
from pyppeteer import launch
from Global.Global import GlobalVal
from utils.Manager.Message_Manager import Message_to_New

logger = Log()
GlobalVal.lock = asyncio.Lock()

config_create()
config = config_load()

if os.path.exists("config/Bot/connect.json"):
    GlobalVal.plugin_list = load_plugins()


async def process_message(event_original_str: str) -> None:
    event_original = json.loads(event_original_str)

    if event_original and "post_type" in event_original:
        Message_json = await Message_to_New(event_original)
        if Message_json:
            event_PostType = Message_json.get("post_type", "none")

            asyncio.create_task(Message_log(event_PostType, Message_json))
            asyncio.create_task(handle_message_cq(event_PostType, Message_json))


async def Message_log(event_PostType: str, Message_json: str) -> None:
    if event_PostType and event_PostType != "心跳包":
        asyncio.create_task(cmd_Log(event_PostType, Message_json))


async def handle_message_cq(event_PostType: str, Message_json: str) -> None:
    if event_PostType == "消息":
        event_Message_From = Message_json["message_type"]

        if event_Message_From == "群聊":
            asyncio.create_task(Plugin_Api.Plugins_Group_Message(Message_json))
        elif event_Message_From == "好友":
            asyncio.create_task(Plugin_Api.Plugins_Friend_Message(Message_json))

    elif event_PostType == "请求":
        asyncio.create_task(Plugin_Api.Plugins_Request(Message_json))

    elif event_PostType == "事件1":
        event_Notice_Type = Message_json["notice_type"]

        if event_Notice_Type == "进群":
            asyncio.create_task(Plugin_Api.Plugins_Notice_join(Message_json))

        if event_Notice_Type == "退群":
            asyncio.create_task(Plugin_Api.Plugins_Notice_leave(Message_json))


async def main() -> None:
    try:
        await (Bot.initialization())

        connect_config = connect_config_load()

        if "perpetua" in connect_config:
            logger.info(message="当前使用perpetua方式连接", flag="Main")
            await (gocq_start_server())
        else:
            logger.error(message="未知接入方式", flag="Main")
    except Exception as e:
        logger.error(message="主程序出错：" + str(e))


async def gocq_start_server() -> None:
    connect_config = connect_config_load()

    host = connect_config["perpetua"]["host"]
    http_port = int(connect_config["perpetua"]["http_port"])
    websocket_port = int(connect_config["perpetua"]["websocket_port"])
    suffix = connect_config["perpetua"]["suffix"]

    if websocket_port == 0:
        logger.info(message="[WS] 正在尝试获取PerPetua-Ws端口", flag="Main")
        try:
            websocket_port = await Bot.perpetua_get_ws_port()
        except Exception as e:
            logger.error(message="获取PerPetua-Ws端口失败：" + str(e))
            exit()

    async with websockets.connect(
        f"ws://{host}:{websocket_port}/{suffix}"
    ) as websocket:
        GlobalVal.websocket = websocket

        logger.info(message="[WS] 成功与PerPetua-Ws建立链接", flag="Main")
        asyncio.create_task(Plugin_Api.Plugins_Start())
        async for message in websocket:
            asyncio.create_task(process_message(message))


if __name__ == "__main__":
    try:
        if config["main"]["Debug"] == "true":
            logger.warning(message="当前调试模式已开启", flag="Main")
        asyncio.run(main())
    except Exception as e:
        logger.error(message="asyncio.run 出错：" + str(e))
    except KeyboardInterrupt:
        asyncio.run(Plugin_Api.Plugins_Stop())
