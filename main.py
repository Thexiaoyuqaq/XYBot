import asyncio
import websockets
import json
from Api import *
from Plugin_Api import *
from Plugin_Manager import load_plugins
from Log import *
from config import load_config
from config import get_config
from pyppeteer import launch
import concurrent.futures

plugins = load_plugins()
load_config('config.ini')
logger = Log()


async def handle_message(event_original: str) -> None:
    """
    处理消息的函数。

    Args:
        event_original (str): 原始消息。

    Returns:
        None
    """
    event_original = json.loads(event_original)
    event_PostType = event_original["post_type"]

    if event_PostType != "meta_event":
        asyncio.create_task(cmd_Log(event_PostType, event_original))

    if event_PostType == "message":
        event_Message_From = event_original["message_type"]

        if event_Message_From == "group":
            asyncio.create_task(Plugins_Group_Message(event_original, plugins))
        elif event_Message_From == "private":
            asyncio.create_task(Plugins_Friend_Message(event_original, plugins))

    if event_PostType == "request":
        asyncio.create_task(Plugins_Request(event_original, plugins))

    if event_PostType == "notice":
        event_Notice_Type = event_original["notice_type"]

        if event_Notice_Type == "group_increase":
            asyncio.create_task(Plugins_Notice_join(event_original, plugins))

        if event_Notice_Type == "group_decrease":
            asyncio.create_task(Plugins_Notice_leave(event_original, plugins))


async def main() -> None:
    """
    主函数。

    Returns:
        None
    """
    try:
        await start_server()
    except Exception as e:
        logger.error(message="主程序出错：" + str(e))


async def start_server() -> None:
    """
    启动 WebSocket 服务器。

    Returns:
        None
    """
    host = get_config('gocq', 'host')
    ws_port = get_config('gocq', 'ws_port')
    logger.info(message="[WS] 等待与Go-CQHTTP建立链接", flag="Main")
    async with websockets.connect('ws://{}:{}'.format(host, ws_port)) as websocket:
        logger.info(message="[WS] 成功与Go-CQHTTP建立链接", flag="Main")
        asyncio.create_task(Plugins_Start(plugins))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                message = await websocket.recv()
                asyncio.create_task(handle_message(message))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(message="asyncio.run 出错：" + str(e))
    except KeyboardInterrupt as e:
        asyncio.create_task(Plugins_Stop(plugins))
        pass
