# -*- coding:utf-8 -*-
# @FileName :LogSys.py
# @Time     : 0:40
# @Author   :Endermite

# 一个简易的日志系统，未来可能用到

import sys
import datetime


class Log:
    """
    简陋的日志发送
    """
    def __init__(self):
        if sys.platform.lower().startswith("win"):
            # 适配windows终端彩色字体，其他系统暂不支持
            self.color_text = self.color_text_windows
        else:
            self.color_text = self.color_text_other

    @staticmethod
    def color_text_other(text: str, color: str) -> str:
        # 放一个占位，防止程序出错
        return text

    @staticmethod
    def color_text_windows(text: str, color: str) -> str:
        """
        可以拿来单独使用
        :param text: 文本
        :param color: 颜色
        """
        colors = {
            'black': 3,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magenta': 5,
            'cyan': 6,
            'white': 7,
        }
        return f"\033[3{colors[color]}m{text}\033[0m"

    def info(self, message: str, flag: str = '') -> None:
        """
        输出info信息
        :param message: 信息
        :param flag: 标记（可选）
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = self.color_text(timestamp, 'green')
        log_type = self.color_text('信息', 'white')
        flag = self.color_text(flag, 'cyan')
        print(f"{timestamp} [{log_type}] {flag}| {message}")

    def warning(self, message: str, flag: str = '') -> None:
        """
        输出warning信息
        :param message: 信息
        :param flag: 标记（可选）
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = self.color_text(timestamp, 'green')
        log_type = self.color_text('警告', 'yellow')
        flag = self.color_text(flag, 'cyan')
        print(f"{timestamp} [{log_type}] {flag}| {message}")

    def error(self, message: str, flag: str = '') -> None:
        """
        输出error信息
        :param message: 信息
        :param flag: 标记（可选）
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = self.color_text(timestamp, 'green')
        log_type = self.color_text('错误', 'red')
        flag = self.color_text(flag, 'cyan')
        print(f"{timestamp} [{log_type}] {flag}| {message}")

    def debug(self, message: str, flag: str = '') -> None:
        """
        输出debug信息
        :param message: 信息
        :param flag: 标记（可选）
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = self.color_text(timestamp, 'green')
        log_type = self.color_text('调试', 'cyan')
        flag = self.color_text(flag, 'cyan')
        print(f"{timestamp} [{log_type}] {flag}| {message}")


