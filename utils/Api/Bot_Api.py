import asyncio
import json
import os
import httpx
from utils.Manager.Config_Manager import config_create, connect_config_load
from utils.Manager.Log_Manager import Log

logger = Log()


class APIWrapper:
    async def initialization(self):
        try:
            config_create()
            asyncio.create_task(self.create_connection_config())
        except Exception as e:
            logger.error(message="初始化失败：" + str(e))

    async def create_connection_config(self):
        if not os.path.exists("config/Bot/connect.json"):
            print("检测到首次运行,正在创建配置文件")
            while True:
                print("对接类型: (回复数字)")
                print("1.perpetua")
                connect_type = input("请输入类型>> ")

                if connect_type == "1":
                    asyncio.create_task(self.create_perpetua_config())
                    break
                else:
                    print("错误的类型，请重新输入。")

    async def create_perpetua_config(self):
        print("请输入perpetua端HTTP端口")
        perpetua_http_port = input("HTTP端口>> ")
        print("请输入perpetua端WebSocket端口  (如果为0则通过自动获取)")
        perpetua_websocket_port = input("WebSocket端口>> ")
        print("请输入HTTP-API端口")
        http_api_port = input("HTTP-API端口>> ")

        config = {
            "perpetua": {
                "host": "127.0.0.1",
                "http_port": int(perpetua_http_port),
                "http_api_port": int(http_api_port),
                "websocket_port": int(perpetua_websocket_port),
                "suffix": "/",
            }
        }

        with open("config/Bot/connect.json", "w") as config_file:
            json.dump(config, config_file)

        input("配置已创建请重新运行程序")
        exit()

    async def perpetua_get_ws_port(self):
        try:
            connect_config = connect_config_load()
            host = connect_config["perpetua"]["host"]
            http_port = connect_config["perpetua"]["http_port"]

            async with httpx.AsyncClient() as client:
                url = f"http://{host}:{http_port}/api/get_ws_port"
                response = await client.get(url)

                if response.status_code == 200:
                    json_data = response.json()
                    ws_port = json_data["data"]["port"]
                    return ws_port
                else:
                    logger.error(
                        message="[系统] 获取WS端口出错，状态码：" + str(response.status_code)
                    )
                    return None
        except Exception as e:
            logger.error(message="获取WS端口出错：" + str(e))


Bot = APIWrapper()
