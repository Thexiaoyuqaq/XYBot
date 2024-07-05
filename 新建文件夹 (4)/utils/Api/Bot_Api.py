import json
import os
from utils.Manager.Config_Manager import config_create
from utils.Manager.Log_Manager import Log
from pyppeteer import launch

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
            print("目前所支持的框架: (回复数字)")
            print("1. Lagrange")
            connect_type = input("请输入类型>> ").strip()

            if connect_type == "1":
                await self.create_perpetua_config()
                break
            else:
                print("错误的类型，请重新输入。")

    async def create_perpetua_config(self):
        websocket_port = self.prompt_input("Lagrange.WebSocket-Port >> ", int)
        http_api_port = self.prompt_input("Lagrange.HTTP-API-Port >> ", int)

        config = {
            "perpetua": {
                "host": "127.0.0.1",
                "http_api_port": http_api_port,
                "websocket_port": websocket_port,
                "suffix": "/",
            }
        }

        os.makedirs(os.path.dirname("config/Bot/"), exist_ok=True)
        with open("config/Bot/connect.json", "w") as config_file:
            json.dump(config, config_file, indent=4)

        input("配置已创建，请重新运行程序")
        exit()

    def prompt_input(self, prompt, cast_type=str):
        while True:
            try:
                return cast_type(input(prompt).strip())
            except ValueError:
                print(f"无效输入，请输入一个{cast_type.__name__}类型的值。")

Bot = APIWrapper()
