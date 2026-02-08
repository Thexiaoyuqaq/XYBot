# API 文档

## 概述

XYQBOT框架提供了丰富的API接口，用于与QQ机器人进行交互。这些API遵循OneBot标准，支持常见的机器人操作。API通过HTTP请求与Lagrange后端通信。

## API分类

### 消息API

#### 发送群消息
- **方法**: `Api.send_group_message(group_id, message, reply_id=None)`
- **功能**: 发送群消息
- **参数**:
  - `group_id` (int): 群号
  - `message` (str): 消息内容
  - `reply_id` (int, optional): 回复消息ID
- **返回**: 消息ID (int) 或 0 (失败)

#### 发送私聊消息
- **方法**: `Api.send_private_message(user_id, message, reply_id=None)`
- **功能**: 发送私聊消息
- **参数**:
  - `user_id` (int): 用户QQ号
  - `message` (str): 消息内容
  - `reply_id` (int, optional): 回复消息ID
- **返回**: 消息ID (int) 或 0 (失败)

#### 撤回消息
- **方法**: `Api.delete_msg(message_id)`
- **功能**: 撤回消息
- **参数**:
  - `message_id` (int): 消息ID
- **返回**: API响应字典

#### 发送群合并消息
- **方法**: `Api.send_group_forward_msg(group_id, messages)`
- **功能**: 发送群合并消息
- **参数**:
  - `group_id` (int): 群号
  - `messages` (list): 消息列表
- **返回**: API响应字典

#### 发送私聊合并消息
- **方法**: `Api.send_private_forward_msg(user_id, messages)`
- **功能**: 发送私聊合并消息
- **参数**:
  - `user_id` (int): 用户QQ号
  - `messages` (list): 消息列表
- **返回**: API响应字典

### 群组API

#### 获取群信息
- **方法**: `Api.get_group_info(group_id, use_cache=False)`
- **功能**: 获取群信息
- **参数**:
  - `group_id` (int): 群号
  - `use_cache` (bool): 是否使用缓存
- **返回**: API响应字典

#### 设置群名片
- **方法**: `Api.set_group_card(group_id, user_id, card="")`
- **功能**: 设置群名片
- **参数**:
  - `group_id` (int): 群号
  - `user_id` (int): 用户QQ号
  - `card` (str): 群名片内容，默认为空字符串
- **返回**: API响应字典

#### 获取群成员列表
- **方法**: `Api.get_group_member_list(group_id, use_cache=True)`
- **功能**: 获取群成员列表
- **参数**:
  - `group_id` (int): 群号
  - `use_cache` (bool): 是否使用缓存
- **返回**: API响应字典

#### 获取群列表
- **方法**: `Api.get_group_list(use_cache=True)`
- **功能**: 获取机器人所在的所有群列表
- **参数**:
  - `use_cache` (bool): 是否使用缓存
- **返回**: API响应字典

### 用户API

#### 获取用户信息
- **方法**: `Api.get_stranger_info(user_id, use_cache=True)`
- **功能**: 获取用户信息
- **参数**:
  - `user_id` (int): 用户QQ号
  - `use_cache` (bool): 是否使用缓存
- **返回**: API响应字典

#### 获取好友列表
- **方法**: `Api.get_friend_list()`
- **功能**: 获取好友列表
- **返回**: API响应字典

### 请求API

#### 处理好友添加请求
- **方法**: `Api.set_friend_add_request(flag, approve, remark=None)`
- **功能**: 处理好友添加请求
- **参数**:
  - `flag` (str): 请求标识
  - `approve` (bool): 是否同意
  - `remark` (str, optional): 备注
- **返回**: API响应字典

#### 处理群添加请求
- **方法**: `Api.set_group_add_request(flag, request_type, approve, reason=None)`
- **功能**: 处理群添加请求
- **参数**:
  - `flag` (str): 请求标识
  - `request_type` (str): 请求类型 (add/invite)
  - `approve` (bool): 是否同意
  - `reason` (str, optional): 拒绝理由
- **返回**: API响应字典

## API使用示例

### Python使用示例

```python
from utils.Api.Command_Api import Api

# 发送群消息
message_id = await Api.send_group_message(123456, "Hello World!")

# 发送私聊消息
message_id = await Api.send_private_message(123456789, "Hello!")

# 获取群信息
group_info = await Api.get_group_info(123456)

# 撤回消息
result = await Api.delete_msg(message_id)

# 设置群名片
result = await Api.set_group_card(123456, 123456789, "新名片")

# 获取用户信息
user_info = await Api.get_stranger_info(123456789)

# 获取群成员列表
members = await Api.get_group_member_list(123456)
```

### 在插件中使用API

```python
from utils.Api.Command_Api import Api

class Plugin:
    async def GroupMessage(self, messageApi, event_original):
        group_id = await messageApi.Get_Group_GroupID()
        user_id = await messageApi.Get_Sender_UserID()
        message = await messageApi.Get_Message_Message()
        
        if message == "你好":
            await Api.send_group_message(group_id, f"你好，{user_id}!")
```

## 底层API方法

除了上述便捷方法外，API还提供了底层方法：

#### 通用API请求
- **方法**: `Api.api_request(endpoint, **params)`
- **功能**: 通用API请求方法
- **参数**:
  - `endpoint` (str): API端点
  - `**params`: API参数
- **返回**: API响应字典

#### POST请求
- **方法**: `Api.post(endpoint, **params)`
- **功能**: 发送POST请求
- **参数**:
  - `endpoint` (str): API端点
  - `**params`: API参数
- **返回**: API响应字典

## API响应格式

所有API调用都会返回字典格式的数据：

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {},
  "message": "",
  "wording": "",
  "echo": ""
}
```

- `status`: 请求状态，"ok"表示成功，"error"表示失败
- `retcode`: 返回码，0表示成功，非0表示失败
- `data`: 返回的数据，根据API不同而变化
- `message`: 错误信息（如果有）
- `wording`: 错误信息（如果有）
- `echo`: 回声，与请求时的echo一致

## 错误处理

当API调用失败时，会返回错误信息：

```python
result = await Api.send_group_message(123456, "Hello")

if "error" in result:
    print(f"API调用失败: {result['error']}")
else:
    print(f"消息发送成功，消息ID: {result}")
```

## 注意事项

1. 所有API调用都是异步的，需要使用`await`关键字
2. API调用可能会失败，建议进行错误处理
3. 部分API需要相应权限才能调用
4. 消息长度有限制，过长的消息会被截断
5. 频繁调用API可能触发频率限制
6. 使用`use_cache`参数可以提高某些API的响应速度
7. 发送消息时，消息ID会在成功时返回，失败时返回0