import os
import json
import asyncio
import traceback
import websockets
from pyppeteer import launch
from utils.Manager.Config_Manager import config_create, config_load, connect_config_load
from utils.Api.Plugin_Api import Plugin_Api
from utils.Api.Bot_Api import Bot
from utils.Manager.Plugin_Manager import PluginManage
from utils.Manager.Log_Manager import Log
from Log import cmd_Log
from Global.Global import GlobalVal
from utils.Manager.Message_Manager import MessageNew

logger = Log()
GlobalVal.lock = asyncio.Lock()

# 初始化配置和插件管理器
config_create()
config = config_load()
plugin_manager = PluginManage(plugin_path="plugins")

# 加载插件（仅在连接配置存在时）
if os.path.exists("config/Bot/connect.json"):
    GlobalVal.plugin_list = plugin_manager.load_plugins()

async def process_message(event_original_str: str) -> None:
    """处理收到的消息"""
    try:
        event_original = json.loads(event_original_str)
        if event_original and "post_type" in event_original:
            Message_json = await MessageNew(event_original)
            if Message_json:
                event_PostType = Message_json.get("post_type", "none")
                await asyncio.gather(
                    Message_log(event_PostType, Message_json),
                    handle_message_cq(event_PostType, Message_json)
                )
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解码错误: {e}")
    except Exception as e:
        logger.error(f"处理消息时发生错误：{traceback.format_exc()}", flag="Main")

async def Message_log(event_PostType: str, Message_json: dict) -> None:
    """记录非心跳包消息"""
    if event_PostType != "心跳包":
        await cmd_Log(event_PostType, Message_json)

async def handle_message_cq(event_PostType: str, Message_json: dict) -> None:
    """根据事件类型处理消息"""
    tasks = []
    if event_PostType == "消息":
        await handle_message_type(Message_json, tasks)
    elif event_PostType == "请求":
        await handle_request_type(Message_json, tasks)
    elif event_PostType == "事件":
        await handle_event_type(Message_json, tasks)

    if tasks:
        await asyncio.gather(*tasks)

async def handle_message_type(Message_json: dict, tasks: list) -> None:
    """处理普通消息"""
    message_type = Message_json.get("message_type", "")
    if message_type == "群聊":
        tasks.append(Plugin_Api.Plugins_Group_Message(Message_json))
    elif message_type == "好友":
        tasks.append(Plugin_Api.Plugins_Private_Message(Message_json))

async def handle_request_type(Message_json: dict, tasks: list) -> None:
    """处理请求消息"""
    request_type = Message_json.get("request_type", "")
    if request_type == "好友请求":
        tasks.append(Plugin_Api.Plugins_Request_Friend(Message_json))
    elif request_type == "群聊请求":
        tasks.append(Plugin_Api.Plugins_Request_Group(Message_json))

async def handle_event_type(Message_json: dict, tasks: list) -> None:
    """处理事件消息"""
    notice_type = Message_json.get("notice_type", "")
    if notice_type == "群成员增加":
        tasks.append(Plugin_Api.Plugins_Notice_GroupIncrease(Message_json))
    elif notice_type == "群成员减少":
        tasks.append(Plugin_Api.Plugins_Notice_GroupDecrease(Message_json))

async def main() -> None:
    """主入口，初始化机器人并建立连接"""
    try:
        await Bot.initialization()
        connect_config = connect_config_load()
        await initialize_connection(connect_config)
    except Exception:
        logger.error(f"主程序出错：{traceback.format_exc()}", flag="Main")

async def initialize_connection(connect_config: dict) -> None:
    """初始化连接"""
    if "perpetua" in connect_config:
        logger.info("当前选用 Lagrange 方式连接", flag="Main")
        await gocq_start_server()
    else:
        logger.error("未知接入方式", flag="Main")

async def gocq_start_server() -> None:
    """启动 WebSocket 服务器"""
    try:
        connect_config = connect_config_load()
        host = connect_config["perpetua"]["host"]
        websocket_port = int(connect_config["perpetua"]["websocket_port"])
        suffix = connect_config["perpetua"]["suffix"]

        async with websockets.connect(f"ws://{host}:{websocket_port}/{suffix}") as websocket:
            GlobalVal.websocket = websocket
            logger.info("[WS] 成功与 Lagrange-Ws 建立链接", flag="Main")

            await Plugin_Api.Plugins_Start()

            async for message in websocket:
                asyncio.create_task(process_message(message))
    except Exception:
        logger.error(f"在连接 WS 出错：{traceback.format_exc()}", flag="Main")

if __name__ == "__main__":
    try:
        if config["main"].get("Debug", "").lower() == "true":
            logger.warning("当前调试模式已开启", flag="Main")
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(Plugin_Api.Plugins_Stop())
        logger.info("程序已终止", flag="Main")
    except Exception:
        logger.error(f"asyncio.run 出错：{traceback.format_exc()}", flag="Main")
