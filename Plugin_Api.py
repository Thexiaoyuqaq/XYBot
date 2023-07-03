import datetime
from LogSys import Log

logger = Log()


async def Plugins_Group_Message(message, plugins):
    """
    处理群消息的逻辑

    Args:
        message (str): 原始消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "GroupMessage") and callable(getattr(plugin, "GroupMessage")):
            try:
                await plugin.GroupMessage(message)
            except Exception as e:
                logger.error(f"[插件] Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][消息][{plugin_name}] 插件缺少 'GroupMessage' 方法，跳过执行。")


async def Plugins_Friend_Message(message, plugins):
    """
    处理群消息的逻辑

    Args:
        message (str): 原始消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "FriendMessage") and callable(getattr(plugin, "FriendMessage")):
            try:
                await plugin.FriendMessage(message)
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][消息][{plugin_name}] 插件缺少 'FriendMessage' 方法，跳过执行。")


async def Plugins_Request(message, plugins):
    """
    处理请求事件的逻辑

    Args:
        message (str): 原始消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Request") and callable(getattr(plugin, "Request")):
            try:
                await plugin.Request(message)
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][事件][请求][{plugin_name}] 插件缺少 'Request' 方法，跳过执行。")


async def Plugins_Notice_join(message, plugins):
    """
    处理进群事件的逻辑

    Args:
        message (str): 原始消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Notice_Group_join") and callable(getattr(plugin, "Notice_Group_join")):
            try:
                await plugin.Notice_Group_join(message)
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][事件][进群][{plugin_name}] 插件缺少 'Notice_join' 方法，跳过执行。")


async def Plugins_Notice_leave(message, plugins):
    """
    处理退群事件的逻辑

    Args:
        message (str): 原始消息
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Notice_Group_leave") and callable(getattr(plugin, "Notice_Group_leave")):
            try:
                await plugin.Notice_Group_leave(message)
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][事件][退群][{plugin_name}] 插件缺少 'Notice_leave' 方法，跳过执行。")


async def Plugins_Start(plugins):
    """
    处理插件启动事件的逻辑

    Args:
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Start") and callable(getattr(plugin, "Start")):
            try:
                await plugin.Start()
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][事件][启动][{plugin_name}] 插件缺少 'Start' 方法，跳过执行。")


async def Plugins_Stop(plugins):
    """
    处理插件卸载事件的逻辑

    Args:
        plugins (list): 插件对象列表

    """
    for plugin_name, plugin in plugins:
        if hasattr(plugin, "Stop") and callable(getattr(plugin, "Stop")):
            try:
                await plugin.Stop()
            except Exception as e:
                logger.error(f"Error: {str(e)}", flag=plugin_name)
        else:
            pass
            # print(event_Time + f"[警告][插件][跳过][事件][关闭][{plugin_name}] 插件缺少 'Stop' 方法，跳过执行。")
