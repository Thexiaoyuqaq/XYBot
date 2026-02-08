# 事件文档

## 概述

XYQBOT框架采用事件驱动架构，支持多种类型的事件。插件可以通过实现特定的事件处理方法来响应不同的事件。

## 事件分类

### 消息事件

#### GroupMessage (群消息事件)
- **触发条件**: 收到群消息时触发
- **处理方法**: `async def GroupMessage(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象，提供便捷的方法获取消息相关信息
  - `event_original`: 原始事件数据
- **示例**:

```python
async def GroupMessage(self, messageApi, event_original):
    group_id = await messageApi.Get_Group_GroupID()  # 获取群号
    user_id = await messageApi.Get_Sender_UserID()   # 获取发送者QQ号
    message = await messageApi.Get_Message_Message() # 获取消息内容
    message_id = await messageApi.Get_Message_ID()   # 获取消息ID
    
    print(f"群 {group_id} 中用户 {user_id} 发送了消息: {message}")
```

#### PrivateMessage (私聊消息事件)
- **触发条件**: 收到私聊消息时触发
- **处理方法**: `async def PrivateMessage(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据
- **示例**:

```python
async def PrivateMessage(self, messageApi, event_original):
    user_id = await messageApi.Get_Sender_UserID()   # 获取发送者QQ号
    message = await messageApi.Get_Message_Message() # 获取消息内容
    message_id = await messageApi.Get_Message_ID()   # 获取消息ID
    
    print(f"用户 {user_id} 发送了私聊消息: {message}")
```

### 通知事件

#### Notice_GroupIncrease (群成员增加事件)
- **触发条件**: 有新成员加入群聊时触发
- **处理方法**: `async def Notice_GroupIncrease(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据
- **示例**:

```python
async def Notice_GroupIncrease(self, messageApi, event_original):
    group_id = await messageApi.get_group_id()       # 获取群号
    user_id = await messageApi.get_sender_id()       # 获取新成员QQ号
    operator_id = await messageApi.get_operator_id() # 获取操作者QQ号
    join_type = await messageApi.get_event_sub_type() # 获取加入类型
    
    print(f"用户 {user_id} 加入了群 {group_id}，操作者: {operator_id}，类型: {join_type}")
```

#### Notice_GroupDecrease (群成员减少事件)
- **触发条件**: 有成员离开群聊时触发
- **处理方法**: `async def Notice_GroupDecrease(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据
- **示例**:

```python
async def Notice_GroupDecrease(self, messageApi, event_original):
    group_id = await messageApi.get_group_id()       # 获取群号
    user_id = await messageApi.get_sender_id()       # 获取离开成员QQ号
    operator_id = await messageApi.get_operator_id() # 获取操作者QQ号
    sub_type = await messageApi.get_event_sub_type() # 获取减少类型
    
    print(f"用户 {user_id} 离开了群 {group_id}，操作者: {operator_id}，类型: {sub_type}")
```

#### Notice_GroupAdmin (群管理员变动事件)
- **触发条件**: 群管理员身份发生变化时触发
- **处理方法**: `async def Notice_GroupAdmin(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_GroupUpload (群文件上传事件)
- **触发条件**: 有成员上传文件到群聊时触发
- **处理方法**: `async def Notice_GroupUpload(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_GroupBan (群禁言事件)
- **触发条件**: 群成员被禁言或解除禁言时触发
- **处理方法**: `async def Notice_GroupBan(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_GroupRecall (群消息撤回事件)
- **触发条件**: 群消息被撤回时触发
- **处理方法**: `async def Notice_GroupRecall(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_FriendRecall (好友消息撤回事件)
- **触发条件**: 好友消息被撤回时触发
- **处理方法**: `async def Notice_FriendRecall(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_FriendAdd (好友添加事件)
- **触发条件**: 好友关系建立时触发
- **处理方法**: `async def Notice_FriendAdd(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_Poke (戳一戳事件)
- **触发条件**: 群内或私聊中发生戳一戳行为时触发
- **处理方法**: `async def Notice_Poke(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

#### Notice_Honor (群荣誉变更事件)
- **触发条件**: 群荣誉（如龙王、群聊之火等）发生变化时触发
- **处理方法**: `async def Notice_Honor(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据

### 请求事件

#### Request_Friend (好友请求事件)
- **触发条件**: 收到好友添加请求时触发
- **处理方法**: `async def Request_Friend(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据
- **示例**:

```python
async def Request_Friend(self, messageApi, event_original):
    user_id = await messageApi.get_sender_id()       # 获取请求者QQ号
    comment = await messageApi.get_request_comment() # 获取验证信息
    flag = await messageApi.get_request_flag()       # 获取请求标识
    
    print(f"用户 {user_id} 申请添加好友，验证信息: {comment}")
```

#### Request_Group (群请求事件)
- **触发条件**: 收到加群请求或邀请时触发
- **处理方法**: `async def Request_Group(self, messageApi, event_original)`
- **参数**:
  - `messageApi`: 消息API对象
  - `event_original`: 原始事件数据
- **示例**:

```python
async def Request_Group(self, messageApi, event_original):
    group_id = await messageApi.get_group_id()       # 获取群号
    user_id = await messageApi.get_sender_id()       # 获取请求者QQ号
    comment = await messageApi.get_request_comment() # 获取验证信息
    flag = await messageApi.get_request_flag()       # 获取请求标识
    sub_type = await messageApi.get_request_type()   # 获取请求类型
    
    print(f"用户 {user_id} 申请加入群 {group_id}，验证信息: {comment}，类型: {sub_type}")
```

### 生命周期事件

#### Start (插件启动事件)
- **触发条件**: 插件启动时触发
- **处理方法**: `async def Start(self)`
- **用途**: 插件初始化、资源加载、定时任务启动等
- **示例**:

```python
async def Start(self):
    print("插件启动，初始化资源...")
    # 启动定时任务
    # 加载配置文件
    # 连接数据库等
```

#### Stop (插件停止事件)
- **触发条件**: 插件停止时触发
- **处理方法**: `async def Stop(self)`
- **用途**: 资源释放、清理工作、保存数据等
- **示例**:

```python
async def Stop(self):
    print("插件停止，清理资源...")
    # 停止定时任务
    # 断开数据库连接
    # 保存配置文件等
```

## 事件处理最佳实践

### 1. 异常处理
```python
async def GroupMessage(self, messageApi, event_original):
    try:
        # 事件处理逻辑
        group_id = await messageApi.Get_Group_GroupID()
        message = await messageApi.Get_Message_Message()

        # 处理消息
        if message == "hello":
            from utils.Api.Command_Api import Api
            await Api.send_group_message(group_id, "Hello!")

    except Exception as e:
        print(f"处理群消息时出错: {e}")
```

### 2. 异步操作
```python
import asyncio

async def GroupMessage(self, messageApi, event_original):
    group_id = await messageApi.Get_Group_GroupID()

    # 使用异步操作
    await asyncio.sleep(1)  # 避免阻塞其他事件处理

    # 发送消息
    from utils.Api.Command_Api import Api
    await Api.send_group_message(group_id, "收到消息")
```

### 3. 条件过滤
```python
async def GroupMessage(self, messageApi, event_original):
    group_id = await messageApi.Get_Group_GroupID()
    user_id = await messageApi.Get_Sender_UserID()
    message = await messageApi.Get_Message_Message()

    # 只处理特定群的消息
    if group_id != 123456:
        return

    # 只处理特定用户的消息
    if user_id != 123456789:
        return

    # 处理消息
    if message.startswith("/"):
        # 处理命令
        pass
```

### 4. 数据持久化
```python
import json

class Plugin:
    def __init__(self):
        self.data_file = "data/plugin_data.json"
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
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
```

## 事件处理注意事项

1. 所有事件处理方法都应该是异步的（使用`async def`）
2. 事件处理过程中发生的异常应该被捕获，否则会影响其他插件
3. 避免在事件处理中使用同步阻塞操作，这会影响事件处理性能
4. 对于耗时较长的操作，建议使用`asyncio.create_task`创建后台任务
5. 事件处理方法的返回值通常会被忽略
6. 事件处理方法应该尽快完成，避免长时间占用事件循环