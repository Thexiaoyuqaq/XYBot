import asyncio
import websockets
import json
from Api import *
from Plugin_Api import *
from Log import *
import asyncio
import datetime
from config import load_config
from config import get_config
from pyppeteer import launch

result = None
plugins = load_plugins()
load_config('config.ini')

async def handle_message(event_original):#消息处理
    event_original = json.loads(event_original)
    event_PostType = event_original["post_type"]
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%H:%M:%S')
    event_Time = "[" + time_str + "]"
    if event_PostType != "meta_event"   :#日志
        await cmd_Log(event_Time,event_PostType,event_original)
    if event_PostType == "message":#消息
        await Plugins_Group_Message(event_original, plugins)
    if event_PostType == "request":#请求
        await Plugins_Request(event_original, plugins)
    if event_PostType == "notice": #事件
        event_Notice_Type = event_original["notice_type"]
        if event_Notice_Type == "group_increase":#群人数增加
            await Plugins_Notice_join(event_original, plugins)
        if event_Notice_Type == "group_decrease":#群人数减少
            await Plugins_Notice_leave(event_original, plugins)
        

async def Message_ServerStuats_class(event_message_Group_ID,event_message_Message_ID): #消息处理-服务器状态
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})  # 根据需要调整视口大小
    await page.setJavaScriptEnabled(enabled=True)
    url = 'http://127.0.0.1:13071/'  # 将"url"替换为你要访问的网页地址
    await page.goto(url)
    screenshot_path = './img/screenshot.png'  # 指定截图保存的路径和文件名
    await page.screenshot({'path': screenshot_path, 'fullPage': True})  # 设置fullPage参数为True，截取整个页面
    await browser.close()
    await send_Groupmessage(event_message_Group_ID,event_message_Message_ID,"[CQ:image,file=http://127.0.0.1:13081/screenshot.png,cache=0]",True)

async def main():#循环主文件 
    try:
        #Remove_Thread = threading.Thread(target=remove_mysql_class)
        #Remove_Thread.start()
        await start_server()
    except Exception as e:
        print("主程序出错：" + str(e))

async def start_server():
    host = get_config('gocq', 'host')
    ws_port = get_config('gocq', 'ws_port')
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%H:%M:%S')
    event_Time = "[" + time_str + "]"
    async with websockets.connect('ws://{}:{}'.format(host,ws_port)) as websocket:
        print(event_Time + f"[信息][系统][WS] Go-CQHTTP协议握手成功")
        async for message in websocket:
            try:
                await handle_message(message)
            except Exception as e:
                print(event_Time + f"[错误][系统][WS][ Error: {str(e)}")
            except KeyboardInterrupt as e:
                pass

try:
    asyncio.run(main())
except Exception as e:
    print("asyncio.run 出错：" + str(e))
except KeyboardInterrupt as e:
    pass
