# XYQBOT机器人框架 - Python

![XYQBOT](https://link_to_your_image.com)

## 简介

XYBot是一个基于Python的QQ机器人框架，旨在简化创建自定义QQ机器人的过程。该框架提供了丰富的功能和工具，以便你能够轻松地构建各种各样的QQ机器人应用。

## 功能特点

- 简单易用的API，适合初学者和有经验的开发者。
- 自定义插件系统，允许用户轻松扩展机器人功能。
- 丰富的机器人API，包括发送消息、管理群组、获取用户信息等等。

## 快速开始

### 安装

1. 克隆这个项目到你的本地环境：

   ```bash
      git clone git@github.com:Thexiaoyuqaq/XYBot.git
      cd XYBot
   
2.安装项目依赖：

   ```bash
      pip install -r requirements.txt

### 2. 配置 Go-CQHTTP

   1.在你的Go-CQHTTP配置文件中，确保已经启用了正向WebSocket和HTTP。
   2.配置WebSocket和HTTP的地址和端口，以便与XYBot框架通信。

### 3. 运行机器人

   在项目根目录下，运行主程序：
   ```bash
      python main.py
   ```
   按照控制台输出的提示信息，填写与Go-CQHTTP对接所需的信息，包括WebSocket地址、端口、API密钥等。

## 插件系统

   XYBot提供了一个强大的插件系统，允许用户自定义和扩展机器人的功能。你可以轻松编写自己的插件，并将其添加到机器人中。以下是如何编写和使用插件的示例：

###编写自定义插件
   1.在项目的 Plugins 目录下创建一个新的Python文件，例如 MyPlugin.py。
   2.按照需求编写你的插件以完善你所需要的功能，以下是一个基础的示例：
```Python
from utils.Api.Command_Api import *

class Plugin:
    async def Notice_Group_join(self, event_original):
        # 加群事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        await send_Groupmessage(group_id, 0, f"欢迎新成员加入，用户ID: {user_id}",False)

    async def Start(self):
        # 启动事件处理逻辑
        #await send_Groupmessage("123456789", 0, "机器人已启动",False)
        pass

    async def Notice_Group_leave(self, event_original):
        # 退群事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        await send_Groupmessage(group_id, 0, f"群成员离开，用户ID: {user_id}",False)

    async def Request(self, event_request_from, event_original):
        # 请求事件处理逻辑
        if event_request_from == "friend":
            # 好友请求处理逻辑
            flag = event_original["flag"]  # 获取Flag
            await set_GroupRequest(flag, True)
        elif event_request_from == "group":
            # 加群请求处理逻辑
            flag = event_original["flag"]  # 获取Flag
            await set_GroupRequest(flag, True)

    async def GroupMessage(self, event_original):
        # 群消息事件处理逻辑
        group_id = event_original["group_id"]  # 获取群组ID
        user_id = event_original["user_id"]  # 获取用户ID
        message = event_original["message"]  # 获取消息内容
        message_id = event_original["message_id"]  # 获取消息内容
        await send_Groupmessage(group_id,message_id, "收到消息Test" ,True)

    async def FriendMessage(self, event_original):
        # 好友消息事件处理逻辑
        user_id = event_original["user_id"]  # 获取用户ID
        message = event_original["message"]  # 获取消息内容
        #await send_PrivateMessage(user_id, f"收到好友消息，消息内容: {message}")
        await send_FriendMessage(user_id,f"收到好友消息，消息内容: {message}")
```

## 贡献

   你可以通过以下方式为项目做出贡献：

   - **提交Bug报告**：如果您发现了任何问题或错误，请[创建一个Bug报告]([https://github.com/your_username/your_qq_bot/issues/new?assignees=&labels=bug&template=bug_report.md&title=](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=BUG&projects=&template=bug_report.md&title=%5BBUG%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Bug%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0))来帮助我们改进。

   - **实现新的功能**：如果您有新功能的想法，欢迎[提交一个功能请求](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=BUG&projects=&template=bug_report.md&title=%5BBUG%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Bug%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0)。我们欢迎社区的贡献。

   - **改进文档**：我们的文档可以改进吗？请随时[提出文档改进建议](https://github.com/Thexiaoyuqaq/XYBot/edit/main/README.md)。您的建议将有助于改善用户体验。

   - **分享这个项目**：如果您喜欢这个项目，不妨在社交媒体上分享它，帮助我们扩大项目的影响力。谢谢您的支持！


## 许可证

   这个项目基于 MIT 许可证 开源。

## 作者

   小雨: 3443135327@qq.com

## 感谢

   在此感谢Go-CQHTTP开发者和本项目的贡献者。
