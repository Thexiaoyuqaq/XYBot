import asyncio
import websockets
import json
from Api import *
from Plugin_Api import *
from Log import *
import datetime
from config import load_config
from config import get_config
from pyppeteer import launch
import concurrent.futures

# 加载插件
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
    # 日志处理
    if event_PostType != "meta_event":
        asyncio.create_task(cmd_Log(event_PostType, event_original))
    # 消息处理
    if event_PostType == "message":
        asyncio.create_task(Plugins_Group_Message(event_original, plugins))
    # 请求处理
    if event_PostType == "request":
        asyncio.create_task(Plugins_Request(event_original, plugins))
    # 事件处理
    if event_PostType == "notice":
        event_Notice_Type = event_original["notice_type"]
        # 群人数增加事件处理
        if event_Notice_Type == "group_increase":
            asyncio.create_task(Plugins_Notice_join(event_original, plugins))
        # 群人数减少事件处理
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
    async with websockets.connect('ws://{}:{}'.format(host, ws_port)) as websocket:
        logger.info(message=f"[信息][系统][WS] Go-CQHTTP协议握手成功")
        # 使用多线程处理消息
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                message = await websocket.recv()
                # 使用异步事件循环在多线程中调用处理消息的函数
                asyncio.create_task(handle_message(message))

try:
    asyncio.run(main())
except Exception as e:
    logger.error(message="asyncio.run 出错：" + str(e))
except KeyboardInterrupt as e:
    pass
