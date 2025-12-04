import os
import sys

def setup_console_output():
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    if sys.platform == 'win32':
        try:
            os.system('chcp 65001 >nul 2>&1')
        except Exception:
            pass
    
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        try:
            if sys.stdout is None or not hasattr(sys.stdout, 'write'):
                sys.stdout = open('bot_stdout.log', 'w', encoding='utf-8', buffering=1)
            if sys.stderr is None or not hasattr(sys.stderr, 'write'):
                sys.stderr = open('bot_stderr.log', 'w', encoding='utf-8', buffering=1)
        except Exception:
            pass
    
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

setup_console_output()

import asyncio
import json
import traceback
import websockets
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import keyboard

from utils.Manager.Config_Manager import config_create, config_load, connect_config_load
from utils.Manager.Event_Manager import EventManager
from utils.Manager.Plugin_Manager import PluginManager
from utils.Manager.Log_Manager import Log
from utils.Api.Bot_Api import Bot
from utils.Api.Plugin_Api import Plugin_Api
from Global.Global import GlobalVal
from pyppeteer import launch

logger = Log()


class BotApplication:
    """主应用类，管理机器人的生命周期"""
    
    def __init__(self):
        self.logger = Log()
        self.event_manager = EventManager()
        self.plugin_manager = PluginManager()
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 5
        
    async def initialize(self):
        """初始化应用程序"""
        try:
            # 初始化配置
            config_create()
            self.config = config_load()
            
            # 初始化Bot API
            await Bot.initialization()
            
            # 初始化全局锁
            GlobalVal.lock = asyncio.Lock()
            
            # 加载插件
            await self.plugin_manager.initialize()
            loaded_count = await self.plugin_manager.load_all_plugins()
            self.logger.info(f"成功加载 {loaded_count} 个插件", flag="Main")

            Plugin_Api.set_plugin_manager(self.plugin_manager)
            
            return True
            
        except Exception as e:
            self.logger.error(f"初始化失败: {traceback.format_exc()}", flag="Main")
            return False
    
    async def process_message(self, message_str: str):
        """处理单条消息"""
        try:
            message_data = json.loads(message_str)
            if not message_data or "post_type" not in message_data:
                return
                
            # 使用事件管理器处理消息
            await self.event_manager.process_event(message_data)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 解析错误: {e}", flag="Main")
        except Exception as e:
            self.logger.error(f"处理消息时发生错误: {traceback.format_exc()}", flag="Main")
    
    @asynccontextmanager
    async def websocket_connection(self, config: Dict[str, Any]):
        """WebSocket连接上下文管理器"""
        host = config["perpetua"]["host"]
        port = config["perpetua"]["websocket_port"]
        suffix = config["perpetua"]["suffix"]
        uri = f"ws://{host}:{port}/{suffix}"
        
        websocket = None
        try:
            websocket = await websockets.connect(uri)
            GlobalVal.websocket = websocket
            self.websocket = websocket
            self.logger.info("[WS] 成功与 Lagrange-Ws 建立链接", flag="Main")
            yield websocket
        finally:
            if websocket:
                GlobalVal.websocket = None
                self.websocket = None
                await websocket.close()
    
    async def handle_websocket(self):
        """处理WebSocket连接和消息"""
        connect_config = connect_config_load()
        
        if not connect_config or "perpetua" not in connect_config:
            self.logger.error("未找到有效的连接配置", flag="Main")
            return
        
        while self.running and self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                async with self.websocket_connection(connect_config) as websocket:
                    self.reconnect_attempts = 0  # 重置重连计数
                    
                    # 触发插件启动事件
                    await self.plugin_manager.trigger_event("Start")
                    
                    # 消息处理循环
                    async for message in websocket:
                        if not self.running:
                            break
                        # 创建任务处理消息，避免阻塞接收
                        asyncio.create_task(self.process_message(message))
                        
            except (websockets.ConnectionClosed, websockets.ConnectionClosedError):
                self.logger.warning("WebSocket连接已关闭", flag="Main")
            except Exception as e:
                self.logger.error(f"WebSocket连接出错: {str(e)}", flag="Main")
            
            if self.running:
                self.reconnect_attempts += 1
                wait_time = min(self.reconnect_delay * self.reconnect_attempts, 60)
                self.logger.info(
                    f"将在 {wait_time} 秒后重试连接 (尝试 {self.reconnect_attempts}/{self.max_reconnect_attempts})",
                    flag="Main"
                )
                await asyncio.sleep(wait_time)
    
    async def run(self):
        """运行主程序"""
        if not await self.initialize():
            self.logger.error("初始化失败，程序退出", flag="Main")
            return
        
        self.running = True
        
        try:
            # 启动WebSocket处理
            await self.handle_websocket()
            
        except KeyboardInterrupt:
            self.logger.info("收到退出信号", flag="Main")
        except Exception as e:
            self.logger.error(f"运行时错误: {traceback.format_exc()}", flag="Main")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """关闭程序"""
        self.running = False
        
        # 触发插件停止事件
        await self.plugin_manager.trigger_event("Stop")
        
        # 关闭WebSocket连接
        if self.websocket:
            await self.websocket.close()
        
        # 卸载所有插件
        await self.plugin_manager.unload_all_plugins()
        
        self.logger.info("程序已正常关闭", flag="Main")


async def main():
    """程序入口"""
    app = BotApplication()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已终止")
        # 添加执行任意键继续
        print("按下任意键继续...")
        keyboard.wait()
        
    except Exception as e:
        print(f"程序异常退出: {e}")
        print("按下任意键继续...")
        keyboard.wait()