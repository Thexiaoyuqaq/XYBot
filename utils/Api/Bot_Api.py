import json
import os
import httpx
from Log import *
from pyppeteer import launch

logger = Log()


class APIWrapper:
    async def initialization(self):
        try:
            if not os.path.exists("config/Bot/connect.json"):
                print("检测到首次运行,正在创建配置文件")
                while True:
                    print("对接类型: (回复数字)")
                    print("1.perpetua")
                    connect_type = input("请输入类型>> ")

                    if connect_type == "1":
                        print("请输入perpetua端HTTP端口")
                        perpetua_http_port = input("HTTP端口>> ")
                        print(
                            "请输入perpetua端WebSocket端口  (如果为0则自动通过HTTP获取)"
                        )
                        perpetua_websocket_port = input("WebSocket端口>> ")

                        config = {
                            "perpetua": {
                                "host": "127.0.0.1",
                                "http_port": int(perpetua_http_port),
                                "websocket_port": int(perpetua_websocket_port),
                                "suffix": "/",
                            }
                        }

                        with open("config/Bot/connect.json", "w") as config_file:
                            json.dump(config, config_file)

                        input("配置已创建请重新运行程序")
                        exit()
                    else:
                        print("错误的类型，请重新输入。")

        except Exception as e:
            logger.error(message="配置文件错误：" + str(e))

    async def perpetua_get_ws_port(self):
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
                print("[系统] 获取WS端口出错，状态码：", response.status_code)
                return None


Bot = APIWrapper()
