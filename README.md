# XYQBOT机器人框架2.0 - Python

![XYQBOT](https://skin.459mc.cn/tu.png)


## 简介

XYBot是一个基于Python，对接PerPetua的框架，旨在简化创建自定义QQ机器人的过程。该框架提供了丰富的功能和工具，以便你能够轻松地构建各种各样的QQ机器人应用。

## 功能特点

- 简单易用的API，适合初学者和有经验的开发者。
- 自定义插件系统，允许用户轻松扩展机器人功能。
- 丰富的机器人API，包括发送消息、管理群组、获取用户信息等。
- API适配，让你在更换了平台但是你的插件无需变动，通用使用

## 实现

<details>
<summary>已实现 API</summary>

### 符合 OneBot 标准的 API

| API                      | 功能                   |
| ------------------------ | ---------------------- |
| /send_group_msg          | [发送群消息]           |
| /get_group_info          | [获取群信息]           |
| /delete_msg          | [撤回消息]           |
| /set_group_add_request          | [操作加群请求]           |
| /set_friend_add_request          | [操作好友请求]           |
| 等待适配      | ..            |

[发送群消息]: https://github.com/botuniverse/onebot-11/blob/master/api/public.md#send_group_msg-%E5%8F%91%E9%80%81%E7%BE%A4%E6%B6%88%E6%81%AF
[获取群信息]: https://github.com/botuniverse/onebot-11/blob/master/api/public.md#get_group_info-%E8%8E%B7%E5%8F%96%E7%BE%A4%E4%BF%A1%E6%81%AF
[处理好友请求]: https://github.com/botuniverse/onebot-11/blob/master/api/public.md#set_friend_add_request-%E5%A4%84%E7%90%86%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82
[处理加群请求]: https://github.com/botuniverse/onebot-11/blob/master/api/public.md#set_group_add_request-%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82%E9%82%80%E8%AF%B7
[撤回信息]: https://github.com/botuniverse/onebot-11/blob/master/api/public.md#delete_msg-%E6%92%A4%E5%9B%9E%E6%B6%88%E6%81%AF
</details>

<details>
<summary>已实现 事件</summary>

### 符合 OneBot 标准的 事件

| 事件                      | 功能                   |
| ------------------------ | ---------------------- |
| 消息          | [Message]           |
| 等待适配      | ..            |

[Message]: https://github.com/botuniverse/onebot-11/blob/master/event/message.md
</details>

## 插件调用器

> 插件调用器 可前往 暂无 查看

- [x] 群聊消息
- [ ] 好友消息
- [x] 事件消息
- [ ] 通知消息

## 快速开始

### 安装

1. 克隆这个项目到你的本地环境：

   ```bash
   git clone git@github.com:Thexiaoyuqaq/XYBot.git
   cd XYBot
   
2.安装项目依赖：

   ```bash
   pip install -r requirements.txt
   ```

### 2. 配置 PerPetua

   1.下载[PerPetua](https://github.com/IUnlimit/perpetua) 并成功登入机器人，具体参考相应文档
   2.注意准备好：在Config文件夹中的config.yml http.port(这是perpetua端HTTP端口)
   3.在appsettings.json中Implementations部分添加
   ```json
   {
      "Type": "Http",
      "Host": "*",
      "Port": 8083, 
      "AccessToken": ""
    }
   ```
   注：记住port端口，这里是HTTP-API端口
   

### 3. 机器人环境配置

   1. 在项目根目录下， 运行main.py
   ```bash
   python main.py
   ```
   按照控制台输出的提示信息，完成首次初始化配置，要求输入PerPetua的HTTP端口以及WS端口,以及http-api端口

## 插件系统

   XYBot提供了一个强大的插件系统，允许用户自定义和扩展机器人的功能。你可以轻松编写自己的插件，并将其添加到机器人中。以下是如何编写和使用插件的示例：

### 编写自定义插件
   #### MessageApi更多数据API 详见：[Plugin_Api.py](https://github.com/Thexiaoyuqaq/XYBot/blob/main/utils/Api/Plugin_Api.py)
   #### Api 更多数据API 详见：[Command_Api.py](https://github.com/Thexiaoyuqaq/XYBot/blob/main/utils/Api/Command_Api.py)
   
   1.在项目的 Plugins 目录下创建一个新的Python文件，例如 MyPlugin.py。
   
   2.按照需求编写你的插件以完善你所需要的功能，以下是一个基础的示例：
   
```Python

from utils.Api.Command_Api import *

Plugin_Info = {
    'name': '示例插件',
    'author': 'xxx',
    'version': '1.0.0'
}

class Plugin:
    def get_plugin_info(self):
      return Plugin_Info

    async def GroupMessage(self,messageApi, event_original):
      #群消息事件处理逻辑
      #获取数据
      group_id = await messageApi.Get_Group_GroupID() #获取群聊ID
      user_id = await messageApi.Get_Sender_UserID()  # 获取用户ID
      message = await messageApi.Get_Message_Message()  # 获取消息内容
      message_id = await messageApi.Get_Message_MessageID()  # 获取消息ID

      if message == "1":
         await Api.send_Groupmessage(group_id,message_id, "1" ,True)
   async def Notice_Group_join(self,messageApi, event_original):
      #群聊加群事件处理逻辑
      #获取数据
      group_id = await messageApi.Get_Group_GroupID()  # 获取群聊ID
      user_id = await messageApi.Get_Sender_UserID()  # 获取用户ID
      operator_id = await messageApi.Get_Operator_UserID()  # 获取操作者ID
      JoinType = await messageApi.Get_User_JoinType()  # 获取加群类型：邀请、主动

      if JoinType == "邀请":
         await Api.send_Groupmessage(group_id,0, f"欢迎 [CQ:at,qq={user_id}] 加入本群，他是通过[CQ:at,qq={operator_id}] 邀请进来的" ,False)
      else:
         await Api.send_Groupmessage(group_id,0, f"欢迎 [CQ:at,qq={user_id}] 加入本群，他是主动进来的" ,False)
   async def Notice_Group_leave(self,messageApi, event_original):
      #群聊退群事件处理逻辑
      #获取数据
      group_id = await messageApi.Get_Group_GroupID()  # 获取群聊ID
      user_id = await messageApi.Get_Sender_UserID()  # 获取用户ID
      operator_id = await messageApi.Get_Operator_UserID()  # 获取操作者ID
      LeaveType = await messageApi.Get_User_LeaveType()  # 获取退群类型：主动、被踢、自己被踢出

      if LeaveType == "主动":
         await Api.send_Groupmessage(group_id,0, f"[CQ:at,qq={user_id}] 主动退群了" ,False)
      elif LeaveType == "被踢":
         await Api.send_Groupmessage(group_id,0, f"[CQ:at,qq={user_id}] 被[CQ:at,qq={operator_id}] 踢出群聊了" ,False)
```

## 待完成事项
- [ ] 完善机器人对接框架的对接度
- [ ] 制作WIKI页面
- [ ] 把插件的固定函数修改为装饰器
- [ ] 完善插件管理器，例如插件信息，插件依赖等功能

## 已完成事项

- [x] 切换至NTQQ框架
- [x] 整理项目结构
- [x] 将API接口内容移植到Api函数下
- [x] 项目实现异步并且线程优化
- [x] 完善README和issues模板
- [x] 排版日志输出（人话：一个日志输出系统）
- [x] 格式化（排版）代码
- [x] 制作一个插件管理器，使得机器人支持加载插件

## 许可证

   这个项目基于 Creative Commons 许可证 开源。

## 作者

   小雨: 3443135327@qq.com

## 贡献

   你可以通过以下方式为项目做出贡献：

   - **提交Bug报告**：如果您发现了任何问题或错误，请[创建一个Bug报告](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=BUG&projects=&template=bug_report.md&title=%5BBUG%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Bug%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0)来帮助我们改进。

   - **实现新的功能**：如果您有新功能的想法，欢迎[提交一个功能请求](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=BUG&projects=&template=bug_report.md&title=%5BBUG%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Bug%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0)。我们欢迎社区的贡献。

   - **分享这个项目**：如果您喜欢这个项目，不妨在社交媒体上分享它，帮助我们扩大项目的影响力。谢谢您的支持！
