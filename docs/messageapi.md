# MessageAPI 文档

## 概述

MessageAPI是XYQBOT框架提供给插件使用的接口，用于获取事件相关的各种信息。它封装了从原始事件数据中提取有用信息的方法，使插件开发者能够方便地获取群组、用户、消息等相关信息。

## MessageAPI接口详解

### 群组相关方法

#### get_group_id()
- **功能**: 获取群组ID
- **适用事件**: `GroupMessage`, `Notice_GroupIncrease`, `Notice_GroupDecrease`, `Request_Group`
- **返回值**: `Optional[int]` - 群号，如果事件不涉及群组则返回None

#### get_group_name()
- **功能**: 获取群组名称
- **适用事件**: `GroupMessage`
- **返回值**: `Optional[str]` - 群名称，如果无法获取则返回None

#### get_group_member_count()
- **功能**: 获取群成员数量
- **适用事件**: `GroupMessage`
- **返回值**: `Optional[int]` - 群成员数量，如果无法获取则返回None

### 发送者相关方法

#### get_sender_id()
- **功能**: 获取发送者ID
- **适用事件**: `GroupMessage`, `PrivateMessage`, `Notice_GroupIncrease`, `Notice_GroupDecrease`
- **返回值**: `Optional[int]` - 发送者QQ号，如果无法获取则返回None

#### get_sender_nickname()
- **功能**: 获取发送者昵称
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `Optional[str]` - 发送者昵称，如果无法获取则返回None

#### get_sender_card()
- **功能**: 获取发送者群名片
- **适用事件**: `GroupMessage`
- **返回值**: `Optional[str]` - 发送者群名片，如果无法获取则返回None

#### get_sender_role()
- **功能**: 获取发送者角色
- **适用事件**: `GroupMessage`
- **返回值**: `Optional[str]` - 发送者角色（如"群主"、"管理"、"群员"），如果无法获取则返回None

### 消息相关方法

#### get_message_content()
- **功能**: 获取消息内容
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `str` - 消息内容，如果无法获取则返回空字符串

#### get_message_id()
- **功能**: 获取消息ID
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `Optional[int]` - 消息ID，如果无法获取则返回None

#### get_message_time()
- **功能**: 获取消息时间
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `Optional[int]` - 消息时间戳，如果无法获取则返回None

#### get_raw_message()
- **功能**: 获取原始消息数据
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `Dict[str, Any]` - 原始消息数据字典

### 请求相关方法

#### get_request_flag()
- **功能**: 获取请求标识
- **适用事件**: `Request_Friend`, `Request_Group`
- **返回值**: `Optional[str]` - 请求标识，用于处理请求时使用

#### get_request_comment()
- **功能**: 获取请求备注
- **适用事件**: `Request_Friend`, `Request_Group`
- **返回值**: `Optional[str]` - 请求备注信息，如好友验证信息或加群理由

#### get_request_type()
- **功能**: 获取请求类型
- **适用事件**: `Request_Group`
- **返回值**: `Optional[str]` - 请求子类型，如"添加"或"邀请"

### 事件相关方法

#### get_operator_id()
- **功能**: 获取操作者ID
- **适用事件**: `Notice_GroupIncrease`, `Notice_GroupDecrease`
- **返回值**: `Optional[int]` - 操作者QQ号，如邀请人或踢人管理员

#### get_event_time()
- **功能**: 获取事件时间
- **适用事件**: `Notice_*`, `Request_*`
- **返回值**: `Optional[int]` - 事件时间戳

#### get_event_sub_type()
- **功能**: 获取事件子类型
- **适用事件**: `Notice_GroupIncrease`, `Notice_GroupDecrease`, `Notice_GroupBan`
- **返回值**: `Optional[str]` - 事件子类型，如"approve"(管理员同意入群)、"invite"(管理员邀请入群)、"leave"(主动退群)、"kick"(成员被踢出)等

## 兼容旧版API方法

为了向后兼容，MessageAPI还提供了与旧版API相同的方法名：

#### Get_Group_GroupID()
- **功能**: 兼容旧API - 获取群组ID
- **适用事件**: `GroupMessage`, `Notice_GroupIncrease`, `Notice_GroupDecrease`, `Request_Group`
- **返回值**: `Optional[int]` - 群号

#### Get_Sender_UserID()
- **功能**: 兼容旧API - 获取发送者ID
- **适用事件**: `GroupMessage`, `PrivateMessage`, `Notice_GroupIncrease`, `Notice_GroupDecrease`
- **返回值**: `Optional[int]` - 发送者QQ号

#### Get_Message_ID()
- **功能**: 兼容旧API - 获取消息ID
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `Optional[int]` - 消息ID

#### Get_Message_Message() / Get_Message_Content()
- **功能**: 兼容旧API - 获取消息内容
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `str` - 消息内容

#### Get_Sender_NickName()
- **功能**: 兼容旧API - 获取发送者昵称
- **适用事件**: `GroupMessage`, `PrivateMessage`
- **返回值**: `str` - 发送者昵称

#### Get_Sender_UserRole()
- **功能**: 兼容旧API - 获取发送者角色
- **适用事件**: `GroupMessage`
- **返回值**: `str` - 发送者角色

#### Get_Operator_UserID()
- **功能**: 兼容旧API - 获取操作者ID
- **适用事件**: `Notice_GroupIncrease`, `Notice_GroupDecrease`
- **返回值**: `Optional[int]` - 操作者QQ号

#### Get_User_JoinType()
- **功能**: 兼容旧API - 获取用户加入类型
- **适用事件**: `Notice_GroupIncrease`
- **返回值**: `Optional[str]` - 加入类型

## 使用示例

### 在插件中使用MessageAPI

```python
class Plugin:
    async def GroupMessage(self, messageApi, event_original):
        # 获取群号
        group_id = await messageApi.get_group_id()
        
        # 获取发送者QQ号
        user_id = await messageApi.get_sender_id()
        
        # 获取消息内容
        message = await messageApi.get_message_content()
        
        # 获取发送者昵称
        nickname = await messageApi.get_sender_nickname()
        
        # 获取发送者群名片
        card = await messageApi.get_sender_card()
        
        # 获取发送者角色
        role = await messageApi.get_sender_role()
        
        # 获取消息ID
        message_id = await messageApi.get_message_id()
        
        print(f"群 {group_id} 中 {nickname}({user_id}) 发送了消息: {message}")

    async def Notice_GroupIncrease(self, messageApi, event_original):
        # 获取群号
        group_id = await messageApi.get_group_id()
        
        # 获取新成员QQ号
        user_id = await messageApi.get_sender_id()
        
        # 获取操作者QQ号（邀请人或同意入群的管理员）
        operator_id = await messageApi.get_operator_id()
        
        # 获取加入类型
        join_type = await messageApi.get_event_sub_type()
        
        print(f"用户 {user_id} 通过 {join_type} 方式加入了群 {group_id}，操作者: {operator_id}")

    async def Request_Friend(self, messageApi, event_original):
        # 获取请求者QQ号
        user_id = await messageApi.get_sender_id()
        
        # 获取验证信息
        comment = await messageApi.get_request_comment()
        
        # 获取请求标识
        flag = await messageApi.get_request_flag()
        
        print(f"用户 {user_id} 申请添加好友，验证信息: {comment}")
```

## 注意事项

1. 所有MessageAPI方法都是异步的，需要使用`await`关键字调用
2. 某些方法只在特定事件类型下有效，对于不适用的事件会返回None
3. MessageAPI会自动缓存部分数据以提高性能
4. 建议在使用返回值前检查是否为None，以避免潜在的错误
5. 旧版API方法仍然可用，但推荐使用新版方法名以获得更好的可读性