import asyncio
from quart import Quart, request
import websockets
import httpx
import json

app = Quart(__name__)

api_open_port = 2333
http_port = 8080


async def forward_to_ws(data):
    perpetua_port = await perpetua_get_ws_port()
    uri = f"ws://127.0.0.1:{perpetua_port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(data))
        async for message in websocket:
            response = json.loads(message)
            post_type = response.get("post_type", "none")
            if post_type == "none":
                print(response)
                asyncio.create_task(websocket.close())
                return response


@app.route("/<endpoint>", methods=["POST"])
async def handle_endpoint(endpoint):
    json_data = await request.get_json()
    message_data = json_data or None
    message_to_send = {"action": endpoint, "params": message_data}
    return await forward_to_ws(message_to_send)


async def perpetua_get_ws_port():
    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:{http_port}/api/get_ws_port"
        try:
            response = await client.get(url)
            if response.status_code == 200:
                json_data = response.json()
                ws_port = json_data["data"]["port"]
                return ws_port
            else:
                print("[系统] 获取WS端口出错，状态码：", response.status_code)
                return None
        except httpx.HTTPError as e:
            print("[系统] 获取WS端口出错：", e)
            return None


if __name__ == "__main__":
    app.run(port=api_open_port, debug=True)
