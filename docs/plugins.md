# 插件开发指南

## 概述

XYQBOT框架提供了灵活的插件系统，允许开发者轻松扩展机器人功能。本指南将详细介绍如何开发、测试和部署插件。

## 插件结构

每个插件都是一个独立的Python文件，必须包含以下元素：

### 1. 插件信息
```python
Plugin_Info = {
    'name': '插件名称',
    'author': '作者',
    'version': '版本号',
    'description': '插件描述',  # 可选
    'dependencies': [],         # 可选
}
```

### 2. 插件主类
```python
class Plugin:
    def __init__(self):
        # 插件初始化代码
        pass

    def get_plugin_info(self):
        return Plugin_Info

    # 事件处理方法
    async def GroupMessage(self, messageApi, event_original):
        # 处理群消息
        pass

    async def PrivateMessage(self, messageApi, event_original):
        # 处理私聊消息
        pass

    async def Start(self):
        # 插件启动时调用
        pass

    async def Stop(self):
        # 插件停止时调用
        pass
```

## 开发步骤

### 第一步：创建插件文件

在`plugins`目录下创建一个新的Python文件，例如`my_plugin.py`：

```python
# plugins/my_plugin.py
from utils.Api.Command_Api import Api

Plugin_Info = {
    'name': '我的插件',
    'author': '开发者姓名',
    'version': '1.0.0',
    'description': '这是一个示例插件'
}

class Plugin:
    def __init__(self):
        # 初始化插件
        self.counter = 0

    def get_plugin_info(self):
        return Plugin_Info

    async def GroupMessage(self, messageApi, event_original):
        # 获取消息信息
        group_id = await messageApi.Get_Group_GroupID()
        user_id = await messageApi.Get_Sender_UserID()
        message = await messageApi.Get_Message_Message()

        # 处理消息
        if message == "/ping":
            await Api.send_group_message(group_id, f"Pong! 用户 {user_id} 调用了ping命令")

    async def PrivateMessage(self, messageApi, event_original):
        # 处理私聊消息
        user_id = await messageApi.Get_Sender_UserID()
        message = await messageApi.Get_Message_Message()

        if message == "/hello":
            await Api.send_private_message(user_id, f"你好，{user_id}!")

    async def Start(self):
        print("我的插件已启动")
        # 可以在这里启动定时任务或其他初始化工作

    async def Stop(self):
        print("我的插件已停止")
        # 可以在这里清理资源或保存数据
```

### 第二步：理解事件处理

插件通过实现特定的事件处理方法来响应不同的事件：

- `GroupMessage`: 处理群消息
- `PrivateMessage`: 处理私聊消息
- `Notice_GroupIncrease`: 处理群成员增加
- `Notice_GroupDecrease`: 处理群成员减少
- `Request_Friend`: 处理好友请求
- `Request_Group`: 处理群请求
- `Start`: 插件启动时调用
- `Stop`: 插件停止时调用

### 第三步：使用API

插件可以通过`utils.Api.Command_Api`模块访问机器人API：

```python
from utils.Api.Command_Api import Api

# 发送群消息
await Api.send_group_message(group_id, message)

# 发送私聊消息
await Api.send_private_message(user_id, message)

# 获取群信息
group_info = await Api.get_group_info(group_id)

# 撤回消息
await Api.delete_msg(message_id)

# 设置群名片
await Api.set_group_card(group_id, user_id, card)
```

### 第四步：获取消息信息

使用`messageApi`对象获取消息相关信息：

```python
async def GroupMessage(self, messageApi, event_original):
    # 获取群号
    group_id = await messageApi.Get_Group_GroupID()
    
    # 获取发送者QQ号
    user_id = await messageApi.Get_Sender_UserID()
    
    # 获取消息内容
    message = await messageApi.Get_Message_Message()
    
    # 获取消息ID
    message_id = await messageApi.Get_Message_ID()
    
    # 获取发送者昵称
    nickname = await messageApi.Get_Sender_NickName()
    
    # 获取发送者角色
    role = await messageApi.Get_Sender_UserRole()
```

## 高级功能

### 1. 数据持久化

插件可以使用文件或数据库来存储数据：

```python
import json
import os

class Plugin:
    def __init__(self):
        self.data_file = "data/my_plugin_data.json"
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    async def GroupMessage(self, messageApi, event_original):
        user_id = await messageApi.Get_Sender_UserID()
        message = await messageApi.Get_Message_Message()

        # 更新数据
        if user_id not in self.data:
            self.data[user_id] = {"count": 0}
        self.data[user_id]["count"] += 1

        # 保存数据
        self.save_data()

    async def Stop(self):
        # 停止时保存数据
        self.save_data()
```

### 2. 定时任务

使用`asyncio`创建定时任务：

```python
import asyncio

class Plugin:
    def __init__(self):
        self.timer_task = None

    async def start_timer(self):
        """启动定时任务"""
        while True:
            try:
                # 执行定时任务
                await self.do_periodic_work()
                
                # 等待一段时间
                await asyncio.sleep(60)  # 每分钟执行一次
            except asyncio.CancelledError:
                # 任务被取消时退出
                break
            except Exception as e:
                print(f"定时任务出错: {e}")

    async def do_periodic_work(self):
        """执行周期性工作"""
        # 例如：向特定群发送每日消息
        from utils.Api.Command_Api import Api
        await Api.send_group_message(123456, "每日提醒：记得喝水！")

    async def Start(self):
        # 启动定时任务
        self.timer_task = asyncio.create_task(self.start_timer())

    async def Stop(self):
        # 停止定时任务
        if self.timer_task:
            self.timer_task.cancel()
            try:
                await self.timer_task
            except asyncio.CancelledError:
                pass
```

### 3. 配置管理

为插件创建配置文件：

```python
import json
import os

class Plugin:
    def __init__(self):
        self.config_file = "config/my_plugin_config.json"
        self.config = self.load_config()

    def load_config(self):
        default_config = {
            "enabled_groups": [],
            "admin_users": [],
            "settings": {
                "max_message_length": 1000,
                "enable_logging": True
            }
        }

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        return default_config

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    async def GroupMessage(self, messageApi, event_original):
        group_id = await messageApi.Get_Group_GroupID()
        
        # 检查群是否在启用列表中
        if group_id not in self.config["enabled_groups"]:
            return

        # 处理消息
        message = await messageApi.Get_Message_Message()
        if message.startswith("/config"):
            # 处理配置命令
            await self.handle_config_command(messageApi, message)
```

## 最佳实践

### 1. 错误处理

始终对可能出错的操作进行错误处理：

```python
async def GroupMessage(self, messageApi, event_original):
    try:
        group_id = await messageApi.Get_Group_GroupID()
        message = await messageApi.Get_Message_Message()
        
        # 处理消息
        if message == "/calc":
            result = await self.calculate_something()
            from utils.Api.Command_Api import Api
            await Api.send_group_message(group_id, f"计算结果: {result}")
            
    except Exception as e:
        # 记录错误但不影响其他插件
        print(f"插件处理消息时出错: {e}")
        
        # 可以向用户发送错误提示
        from utils.Api.Command_Api import Api
        await Api.send_group_message(group_id, "处理命令时出错，请稍后再试")
```

### 2. 异步编程

避免使用同步阻塞操作：

```python
import asyncio
import aiohttp  # 使用异步HTTP库而不是requests

class Plugin:
    async def fetch_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def GroupMessage(self, messageApi, event_original):
        message = await messageApi.Get_Message_Message()
        
        if message == "/weather":
            try:
                # 使用异步操作获取天气数据
                weather_data = await self.fetch_data("https://api.weather.com/...")
                from utils.Api.Command_Api import Api
                await Api.send_group_message(
                    await messageApi.Get_Group_GroupID(),
                    f"天气信息: {weather_data}"
                )
            except Exception as e:
                print(f"获取天气数据失败: {e}")
```

### 3. 资源管理

正确管理资源，避免内存泄漏：

```python
class Plugin:
    def __init__(self):
        self.connections = {}
        self.timers = []

    async def cleanup(self):
        """清理资源"""
        # 关闭连接
        for conn in self.connections.values():
            if hasattr(conn, 'close'):
                await conn.close()
        self.connections.clear()

        # 取消定时器
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()

    async def Stop(self):
        await self.cleanup()
```

## 调试技巧

### 1. 日志记录

在开发过程中添加日志记录：

```python
async def GroupMessage(self, messageApi, event_original):
    print(f"插件收到群消息: {await messageApi.Get_Message_Message()}")
    
    # 处理逻辑
    # ...
    
    print("消息处理完成")
```

### 2. 测试插件

创建简单的测试插件来验证功能：

```python
# test_plugin.py
from utils.Api.Command_Api import Api

Plugin_Info = {
    'name': '测试插件',
    'author': 'Developer',
    'version': '1.0.0',
    'description': '用于测试功能的插件'
}

class Plugin:
    def get_plugin_info(self):
        return Plugin_Info

    async def GroupMessage(self, messageApi, event_original):
        group_id = await messageApi.Get_Group_GroupID()
        user_id = await messageApi.Get_Sender_UserID()
        message = await messageApi.Get_Message_Message()
        
        if message == "/test":
            await Api.send_group_message(group_id, f"测试成功！来自用户: {user_id}")

    async def Start(self):
        print("测试插件已启动")

    async def Stop(self):
        print("测试插件已停止")
```

## 常见问题

### Q: 插件不生效怎么办？
A: 检查以下几点：
1. 插件文件是否放在`plugins`目录下
2. 插件文件名是否符合命名规范（不含特殊字符）
3. 插件类名是否为`Plugin`
4. 是否有语法错误

### Q: 如何在插件中使用第三方库？
A: 在插件文件顶部导入所需库，确保库已安装：
```python
import requests  # 需要先安装: pip install requests
```

### Q: 插件如何与其他插件通信？
A: 目前插件间通信主要通过共享数据文件或数据库实现，后续版本可能会提供插件间通信机制。

### Q: 插件如何处理大量数据？
A: 对于大量数据处理，建议：
1. 使用异步操作避免阻塞
2. 分批处理数据
3. 使用数据库而非文件存储
4. 实现进度反馈机制

## 示例插件

下面是一个功能完整的示例插件：

```python
# plugins/example_plugin.py
import json
import os
import asyncio
from utils.Api.Command_Api import Api

Plugin_Info = {
    'name': '示例插件',
    'author': 'Example Author',
    'version': '1.0.0',
    'description': '一个功能完整的示例插件'
}

class Plugin:
    def __init__(self):
        self.data_file = "data/example_plugin.json"
        self.user_data = self.load_data()
        self.admin_users = [3443135327]  # 管理员QQ号

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}, "stats": {"messages_processed": 0}}

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_data, f, ensure_ascii=False, indent=2)

    def get_plugin_info(self):
        return Plugin_Info

    async def GroupMessage(self, messageApi, event_original):
        try:
            group_id = await messageApi.Get_Group_GroupID()
            user_id = await messageApi.Get_Sender_UserID()
            message = await messageApi.Get_Message_Message()

            # 更新统计数据
            self.user_data["stats"]["messages_processed"] += 1
            
            # 初始化用户数据
            if str(user_id) not in self.user_data["users"]:
                self.user_data["users"][str(user_id)] = {"count": 0, "last_message": ""}
            self.user_data["users"][str(user_id)]["count"] += 1
            self.user_data["users"][str(user_id)]["last_message"] = message

            # 处理命令
            if message == "/stats":
                user_stats = self.user_data["users"][str(user_id)]
                total_messages = self.user_data["stats"]["messages_processed"]
                
                response = f"""📊 统计信息
你的消息数: {user_stats['count']}
总处理消息数: {total_messages}
最后一条消息: {user_stats['last_message']}"""
                
                await Api.send_group_message(group_id, response)

            elif message == "/reset" and user_id in self.admin_users:
                self.user_data = {"users": {}, "stats": {"messages_processed": 0}}
                await Api.send_group_message(group_id, "统计已重置")

            elif message.startswith("/echo "):
                echo_text = message[6:]  # 移除"/echo "前缀
                await Api.send_group_message(group_id, f"你说: {echo_text}")

            # 保存数据
            self.save_data()

        except Exception as e:
            print(f"示例插件处理消息时出错: {e}")

    async def Start(self):
        print("示例插件已启动")
        # 可以在这里进行初始化工作

    async def Stop(self):
        print("示例插件已停止")
        # 保存数据
        self.save_data()
```

这个指南涵盖了插件开发的主要方面，希望对你有所帮助！
