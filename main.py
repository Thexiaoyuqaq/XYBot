import asyncio
import websockets
import json
import concurrent.futures
import threading
from Log import *
from utils.Api.Plugin_Api import *
from utils.Manager.Plugin_Manager import load_plugins
from utils.Manager.Config_Manager import *
from pyppeteer import launch
from flask import Flask, request, jsonify
app = Flask(__name__)

logger = Log()
config_create()
config = config_load()
if os.path.exists('config/Bot/connect.ini'):
    plugins = load_plugins()


async def handle_message_cq(event_original: str) -> None:
    """
    GOCQ-HTTP处理消息的函数。

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
                    print("对接DChat会以Webhook方式接收消息,让DChat收到消息后调用你留的Webhook地址来获取消息,也就是说必须处于公网下")
                    print("Webhook开放的端口")
                    webhook_port = input()
                    print("请输入ApiKey")
                    apikey = input()
                    config = {
                        "dchat": {
                            "dchat_local_flask_host": "0.0.0.0",
                            "dchat_local_flask_port": int(webhook_port),
                            "dchat_apikey": apikey
                        }
                    }
                    with open("config/Bot/connect.ini", "w") as config_file:
                        json.dump(config, config_file)
                    input("配置已创建请重新运行程序")
                    break
                else:
                    print("错误的类型，请重新输入。")
        else:
            connect_config = connect_config_load()
            if "gocq" in connect_config:
                logger.info(message="当前使用GO-CQHTTP方式连接", flag="Main")
                await gocq_start_server()
            elif "dchat" in connect_config:
                logger.info(message="当前使用DChat方式连接", flag="Main")
                await dchat_start_server()
    except Exception as e:
        logger.error(message="主程序出错：" + str(e))


async def dchat_start_server() -> None:
    connect_config = connect_config_load()
    """
    启动 WebSocket 服务器。

    Returns:
        None
    """
    flask_host = connect_config["dchat"]["dchat_local_flask_host"]
    flask_port = connect_config["dchat"]["dchat_local_flask_port"]
    asyncio.create_task(Plugins_Start(plugins))
    logger.info(message="[Webhook] 开放在{}:{}/webhook".format(flask_host,int(flask_port)), flag="Main")
    app.run(host=flask_host, port=int(flask_port))
    
async def handle_message_dc(data):
    From_type = data["target"]
    if "gid" in From_type:
        new_json = {
            "from" : "group",
            "message": data["detail"]["content"],
            "message_id": data["mid"],
            "user_id": data["from_uid"],
            "group_id": data["target"]["gid"]
        }
    if "uid" in From_type:
        new_json = {
            "from" : "private",
            "message": data["detail"]["content"],
            "message_id": data["mid"],
            "user_id": data["from_uid"],
        }
    event_Message_From = new_json["from"]
    asyncio.create_task(cmd_Log("message2", new_json))
    if event_Message_From == "group":
        asyncio.create_task(Plugins_Group_Message(new_json, plugins))
    elif event_Message_From == "private":
        asyncio.create_task(Plugins_Friend_Message(new_json, plugins))

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    data = request.json
    with concurrent.futures.ThreadPoolExecutor():
        threading.Thread(target=handle_message_dc,args=(data,))
        asyncio.run(handle_message_dc(data))
    return jsonify(data)


async def gocq_start_server() -> None:
    connect_config = connect_config_load()
    """
    启动 WebSocket 服务器。

    Returns:
        None
    """
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
        asyncio.run(main())
    except Exception as e:
        logger.error(message="asyncio.run 出错：" + str(e))
    except KeyboardInterrupt as e:
        asyncio.run(Plugins_Stop(plugins))