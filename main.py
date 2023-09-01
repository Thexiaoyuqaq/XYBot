import os
import json
import asyncio
import websockets
import concurrent.futures
from Log import *
from utils.Api.Plugin_Api import *
from utils.Manager.Plugin_Manager import load_plugins
from utils.Manager.Config_Manager import config_create, config_load, connect_config_load
from pyppeteer import launch

logger = Log()
config_create()
config = config_load()
if os.path.exists('config/Bot/connect.ini'):
    plugins = load_plugins()

async def handle_message_cq(event_original: str) -> None:
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
    try:
        if not os.path.exists('config/Bot/connect.ini'):
            print("检测到首次运行,正在创建配置文件")
            while True:
                print("对接类型: (回复数字)")
                print("1.Go-CQHTTP")
                print("2.DChat")
                connect_type = input()

                if connect_type == "1":
                    print("请输入Go-CQHTTP的HTTP接口端口")
                    cq_http_port = input()
                    print("请输入Go-CQHTTP的正向WebSocket接口端口")
                    cq_websocket_port = input()
                    config = {
                        "gocq": {
                            "cq_host": "127.0.0.1",
                            "cq_http_port": cq_http_port,
                            "cq_websocket_port": cq_websocket_port
                        }
                    }
                    with open("config/Bot/connect.ini", "w") as config_file:
                        json.dump(config, config_file)
                    input("配置已创建请重新运行程序")
                    break
                elif connect_type == "2":
                    print("DChat已弃用")
                else:
                    print("错误的类型，请重新输入。")
        else:
            connect_config = connect_config_load()
            if "gocq" in connect_config:
                logger.info(message="当前使用GO-CQHTTP方式连接", flag="Main")
                await gocq_start_server()
            else:
                logger.error(message="未知接入方式",flag="Main")
    except Exception as e:
        logger.error(message="主程序出错：" + str(e))

async def gocq_start_server() -> None:
    connect_config = connect_config_load()
    host = connect_config["gocq"]["cq_host"]
    ws_port = connect_config["gocq"]["cq_websocket_port"]
    logger.info(message="[WS] 等待与Go-CQHTTP建立链接", flag="Main")
    async with websockets.connect('ws://{}:{}'.format(host, ws_port)) as websocket:
        logger.info(message="[WS] 成功与Go-CQHTTP建立链接", flag="Main")
        asyncio.create_task(Plugins_Start(plugins))
        with concurrent.futures.ThreadPoolExecutor():
            while True:
                message = await websocket.recv()
                asyncio.create_task(handle_message_cq(message))

if __name__ == "__main__":
    try:
        if config["main"]["Debug"] == "true":
            logger.warning(message="当前调试模式已开启", flag="Main")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(message="asyncio.run 出错：" + str(e))
    except KeyboardInterrupt as e:
        loop.run_until_complete(Plugins_Stop(plugins))
