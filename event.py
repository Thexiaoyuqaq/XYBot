# -*- coding:utf-8 -*-
# @FileName :event.py
# @Time     : 6:01
# @Author   :Endermite

# 将Plugin_Api.py中的事件处理拆分
import asyncio
from Plugin_Manager import load_plugins
from LogSys import Log
import inspect

logger = Log()
pluginList = load_plugins()


async def handle_event(event: str, original_message):
    for plugin in pluginList:
        if inspect.ismethod(getattr(plugin[1], event, False)):
            try:
                method = getattr(plugin[1], event)
                await method(original_message)
            except:
                logger.error(message=str(e), flag=plugin[0])


async def privateMessageEvent(original_message):
    """
    私聊消息事件
    """
    asyncio.create_task(handle_event(event="privateMessageEvent", original_message=original_message))


async def groupMessageEvent(original_message):
    """
    群聊消息事件
    """
    asyncio.create_task(handle_event(event="groupMessageEvent", original_message=original_message))


async def tempMessageEvent(original_message):
    """
    临时消息事件
    """
    asyncio.create_task(handle_event(event="tempMessageEvent", original_message=original_message))

