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
            await self.create_connection_config()
        except Exception as e:
            logger.error(message="初始化失败：" + str(e))

    async def create_connection_config(self):
        config_path = "config/Bot/connect.json"
        if not os.path.exists(config_path):
            print("检测到首次运行,正在创建配置文件")
            await self.prompt_connection_type()

    async def prompt_connection_type(self):
        while True:
            print("对接类型: (回复数字)")
            print("1. perpetua")
            connect_type = input("请输入类型>> ").strip()

            if connect_type == "1":
                await self.create_perpetua_config()
                break
            else:
                print("错误的类型，请重新输入。")

    async def create_perpetua_config(self):
        perpetua_http_port = self.prompt_input("请输入perpetua端HTTP端口>> ", int)
        perpetua_websocket_port = self.prompt_input("请输入perpetua端WebSocket端口 (如果为0则通过自动获取)>> ", int)
        http_api_port = self.prompt_input("请输入HTTP-API端口>> ", int)

        config = {
            "perpetua": {
                "host": "127.0.0.1",
                "http_port": perpetua_http_port,
                "http_api_port": http_api_port,
                "websocket_port": perpetua_websocket_port,
                "suffix": "/",
            }
        }

        os.makedirs(os.path.dirname("config/Bot/"), exist_ok=True)
        with open("config/Bot/connect.json", "w") as config_file:
            json.dump(config, config_file, indent=4)

        input("配置已创建请重新运行程序")
        exit()

    def prompt_input(self, prompt, cast_type=str):
        while True:
            try:
                return cast_type(input(prompt).strip())
            except ValueError:
                print(f"无效输入，请输入一个{cast_type.__name__}类型的值。")

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
                    return json_data["data"]["port"]
                else:
                    logger.error(
                        message=f"[系统] 获取WS端口出错，状态码：{response.status_code}"
                    )
                    return None
        except Exception as e:
            logger.error(message="获取WS端口出错：" + str(e))
            return None


Bot = APIWrapper()
