import json
import os
import asyncio
from utils.Manager.Config_Manager import config_create
from utils.Manager.Log_Manager import Log

logger = Log()

class APIWrapper:
    async def initialization(self):
        """
        初始化配置管理与连接配置。
        """
        try:
            config_create()  # 初始化基础配置
            await self.create_connection_config()
        except Exception as e:
            logger.error(f"初始化失败：{str(e)}")

    async def create_connection_config(self):
        """
        检查并创建连接配置文件，如果不存在则引导用户创建。
        """
        config_path = "config/Bot/connect.json"
        if not os.path.exists(config_path):
            print("检测到首次运行，正在创建配置文件...")
            await self.prompt_connection_type()

    async def prompt_connection_type(self):
        """
        引导用户选择连接框架类型。
        """
        options = {
            "1": ("Lagrange", self.create_lagrange_config)
        }
        while True:
            print("目前所支持的框架: (回复数字)")
            for key, (name, _) in options.items():
                print(f"{key}. {name}")

            choice = input("请输入类型 >> ").strip()
            if choice in options:
                _, create_func = options[choice]
                await create_func()
                break
            else:
                print("错误的类型，请重新输入。")

    async def create_lagrange_config(self):
        """
        创建 Lagrange 框架的连接配置文件。
        """
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

        self.save_config("config/Bot/connect.json", config)
        print("配置已创建，请重新运行程序。")
        exit()

    def prompt_input(self, prompt, cast_type=str):
        """
        提示用户输入并转换为指定类型。

        参数:
            prompt (str): 输入提示信息。
            cast_type (type): 期望的输入类型。
        
        返回:
            转换后的用户输入。
        """
        while True:
            try:
                return cast_type(input(prompt).strip())
            except ValueError:
                print(f"无效输入，请输入一个 {cast_type.__name__} 类型的值。")

    def save_config(self, path, config):
        """
        将配置保存到指定路径。

        参数:
            path (str): 配置文件路径。
            config (dict): 配置信息。
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as config_file:
            json.dump(config, config_file, indent=4)

# 实例化并初始化 APIWrapper
Bot = APIWrapper()
