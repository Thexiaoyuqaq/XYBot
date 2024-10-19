# -*- coding:utf-8 -*-
# @FileName :LogSys.py
# @Time     : 0:40
# @Author   :Endermite

import sys
import datetime
import os
from enum import Enum


class LogLevel(Enum):
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    DEBUG = "调试"


class Log:
    """
    简陋的日志发送
    """

    def __init__(self, log_to_file=False):
        self.log_to_file = log_to_file
        if sys.platform.lower().startswith("win"):
            self.color_text = self.color_text_windows
        else:
            self.color_text = self.color_text_other
        self.log_file_path = "log.txt"

        # 如果启用文件日志，确保日志文件存在
        if self.log_to_file:
            with open(self.log_file_path, "a") as f:
                f.write("日志系统启动\n")

    def generate_timestamp(self):
        """生成当前时间戳"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def color_text_other(text: str, color: str) -> str:
        # 放一个占位，防止程序出错
        return text

    @staticmethod
    def color_text_windows(text: str, color: str) -> str:
        """ Windows终端彩色文本 """
        colors = {
            "black": 3,
            "red": 1,
            "green": 2,
            "yellow": 3,
            "blue": 4,
            "magenta": 5,
            "cyan": 6,
            "white": 7,
        }
        return f"\033[3{colors[color]}m{text}\033[0m"

    def log(self, level: LogLevel, message: str, flag: str = "") -> None:
        """ 通用日志方法 """
        timestamp = self.generate_timestamp()
        colored_timestamp = self.color_text(timestamp, "green")
        colored_flag = self.color_text(flag, "cyan")
        log_type = self.color_text(level.value, self.get_color_for_level(level))

        log_message = f"{colored_timestamp} [{log_type}] {colored_flag}| {message}"
        print(log_message)

        # 写入文件日志
        if self.log_to_file:
            with open(self.log_file_path, "a") as f:
                f.write(f"{log_message}\n")

    def get_color_for_level(self, level: LogLevel) -> str:
        """ 根据日志级别返回颜色 """
        if level == LogLevel.INFO:
            return "white"
        elif level == LogLevel.WARNING:
            return "yellow"
        elif level == LogLevel.ERROR:
            return "red"
        elif level == LogLevel.DEBUG:
            return "cyan"

    def info(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.INFO, message, flag)

    def warning(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.WARNING, message, flag)

    def error(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.ERROR, message, flag)

    def debug(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.DEBUG, message, flag)