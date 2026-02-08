# XYQBOT机器人框架2.0 - Python

![XYQBOT](https://skin.459mc.cn/tu.png)

## 目录

- [简介](#简介)
- [功能特点](#功能特点)
- [快速开始](#快速开始)
- [架构概览](#架构概览)
- [API参考](#api参考)
- [事件系统](#事件系统)
- [插件系统](#插件系统)
- [插件开发](#插件开发)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [文档](#文档)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 简介

XYBot是一个基于Python，以Lagrange为基础的QQ机器人框架，旨在简化创建自定义QQ机器人的过程。该框架提供了丰富的功能和工具，以便你能够轻松地构建各种各样的QQ机器人应用。

## 功能特点

- **简单易用的API**：适合初学者和有经验的开发者
- **灵活的插件系统**：允许用户轻松扩展机器人功能
- **丰富的机器人API**：包括发送消息、管理群组、获取用户信息等
- **异步高性能**：采用asyncio实现高并发处理能力
- **完整的事件系统**：支持消息、通知、请求等多种事件类型
- **智能日志系统**：提供彩色日志输出和分类记录

## 快速开始

### 环境要求

- Python 3.9+
- Windows/Linux

### 安装步骤

1. 克隆项目到本地：

```bash
git clone https://github.com/Thexiaoyuqaq/XYBot.git
cd XYBot
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

### 配置 NapCat 连接

1. 从 [NapCat Releases](https://github.com/NapNeko/NapCatQQ/releases) 获取最新版
2. (1):将下载后的 `NapCat.Shell.Windows.Node.zip` 放入项目根目录并解压单独文件夹
3. (2):再下载 [9.9.26-44343 X64 Win](https://dldir1.qq.com/qqfile/qq/QQNT/40d6045a/QQ9.9.26.44343_x64.exe)
4. 先安装 QQ 9.9.26-44343
5. 然后启动 NapCat，扫码进行登录
6. 通过 控制台输出的WebUI 打开浏览器面板点击 网络配置
6. 添加一个 HTTP服务器 及 Websockets服务器 （记住端口）

### 运行机器人

1. 在项目根目录下运行：

```bash
python main.py
```

2. 按照控制台提示逐步填写 HTTP-API-PORT，WebSocket-PORT 相关配置项
3. 填写完成后，程序自动退出，请重新运行
4. 等待出现连接成功的提示

## 架构概览

XYQBOT采用模块化架构，主要包括以下几个核心组件：

- **主程序** (`main.py`): 机器人主程序，负责整个生命周期管理，包括WebSocket连接、消息处理、插件管理等
- **插件管理器** (`utils/Manager/Plugin_Manager.py`): 负责插件的加载、卸载、重载和事件分发
- **事件管理器** (`utils/Manager/Event_Manager.py`): 负责事件的接收、处理和分发到对应的插件
- **API层** (`utils/Api/`): 提供与机器人交互的API接口，包括Bot_API、Command_API和Plugin_API
- **日志系统** (`utils/Manager/Log_Manager.py`): 提供彩色日志输出功能和分类记录
- **消息处理器** (`utils/MessageNew/`): 负责将原始消息转换为标准化格式
- **配置管理器** (`utils/Manager/Config_Manager.py`): 负责管理主配置和连接配置

这种架构设计使XYQBOT具有高度的可扩展性和灵活性，开发者可以轻松地添加新功能而不影响核心系统。

## API参考

XYQBOT提供了丰富的API接口，用于与QQ机器人进行交互。这些API遵循OneBot标准，支持常见的机器人操作。

> 更多API详情请参阅 [API文档](./docs/api.md)

## 事件系统

XYQBOT采用事件驱动架构，支持多种类型的事件。插件可以通过实现特定的事件处理方法来响应不同的事件。

> 更多事件详情请参阅 [事件文档](./docs/events.md)

## 插件系统

XYQBOT提供了强大的插件系统，允许用户通过编写插件来扩展机器人功能。插件系统具有以下特点：

- **热加载/卸载**: 支持在不停机的情况下动态加载和卸载插件
- **事件驱动**: 支持多种事件类型，包括消息事件、通知事件和请求事件
- **生命周期管理**: 支持插件启动和停止事件，便于资源管理
- **统一API**: 所有插件都可以通过统一的API接口与机器人交互

插件位于 `plugins/` 目录下，每个插件都是一个独立的Python文件，实现了特定的接口。系统内置插件管理命令，可通过群聊指令管理插件。

## 插件开发

> 详细插件开发指南请参阅 [插件开发文档](./docs/plugins.md)

## 配置说明

### 主配置文件 (config/Bot/config.json)

```json
{
    "main": {
        "Debug": "False",
        "master_qq": "123456"
    }
}
```

### 连接配置文件 (config/Bot/connect.json)

```json
{
    "perpetua": {
        "host": "127.0.0.1",
        "http_api_port": 8083,
        "websocket_port": 8080,
        "suffix": "/"
    }
}
```

## 常见问题

### Q: 如何添加新插件？
A: 在 `plugins` 目录下创建新的 `.py` 文件，按照插件结构编写代码即可。

## 文档

了解更多关于XYQBOT的信息，请查阅以下文档：

- [API参考](./docs/api.md) - 详细的API接口说明
- [事件系统](./docs/events.md) - 事件处理机制和可用事件
- [MessageAPI参考](./docs/messageapi.md) - MessageAPI接口详细说明
- [插件开发指南](./docs/plugins.md) - 如何开发和管理插件

## 贡献指南

### 你可以通过以下方式为项目做出贡献：

- **提交Bug报告**：如果您发现了任何问题或错误，请[创建一个Bug报告](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=BUG&projects=&template=bug_report.md&title=%5BBUG%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Bug%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0)来帮助我们改进。

- **实现新的功能**：如果您有新功能的想法，欢迎[提交一个功能请求](https://github.com/Thexiaoyuqaq/XYBot/issues/new?assignees=&labels=feature&projects=&template=feature_request.md&title=%5BFEATURE%5D+-+%E5%9C%A8%E6%AD%A4%E5%A1%AB%E5%86%99Feature%E7%9A%84%E7%AE%80%E8%A6%81%E6%8F%8F%E8%BF%B0)。我们欢迎社区的贡献。

- **分享这个项目**：如果您喜欢这个项目，不妨在社交媒体上分享它，帮助我们扩大项目的影响力。谢谢您的支持！

### 代码贡献流程：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

这个项目基于 Creative Commons 许可证开源。

## 作者

小雨: 3443135327@qq.com

## 致谢

感谢所有为XYQBOT项目做出贡献的开发者们！
