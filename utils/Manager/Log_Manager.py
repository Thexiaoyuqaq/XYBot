# -*- coding:utf-8 -*-
# Log_Manager.py

import sys
import os
import datetime
from enum import Enum


class LogLevel(Enum):
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    DEBUG = "调试"


class Log:
    """日志系统"""

    def __init__(self, log_to_file=False):
        self.log_to_file = log_to_file
        
        # 检测是否在 PyInstaller 打包环境中运行
        self.is_frozen = getattr(sys, 'frozen', False)
        
        if sys.platform.lower().startswith("win"):
            self.color_text = self.color_text_windows
        else:
            self.color_text = self.color_text_other
            
        self.log_file_path = "log.txt"

        # 强制设置输出编码和缓冲
        self._setup_output()

        if self.log_to_file:
            with open(self.log_file_path, "a", encoding='utf-8') as f:
                f.write("日志系统启动\n")

    def _setup_output(self):
        """设置标准输出，确保打包后能正常输出"""
        # Windows 控制台强制 UTF-8
        if sys.platform == 'win32':
            try:
                os.system('chcp 65001 >nul 2>&1')
            except Exception:
                pass
        
        try:
            # 强制 UTF-8 编码
            if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
            if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
        except Exception:
            pass
        
        if self.is_frozen:
            if sys.stdout is None:
                sys.stdout = open('stdout.log', 'w', encoding='utf-8', buffering=1)
            if sys.stderr is None:
                sys.stderr = open('stderr.log', 'w', encoding='utf-8', buffering=1)

    def generate_timestamp(self):
        """生成当前时间戳"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def color_text_other(text: str, color: str) -> str:
        return text

    @staticmethod
    def color_text_windows(text: str, color: str) -> str:
        """Windows终端彩色文本"""
        colors = {
            "black": 0, "red": 1, "green": 2, "yellow": 3,
            "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
        }
        return f"\033[3{colors.get(color, 7)}m{text}\033[0m"

    def log(self, level: LogLevel, message: str, flag: str = "") -> None:
        """通用日志方法 - 修复打包后输出问题"""
        timestamp = self.generate_timestamp()
        colored_timestamp = self.color_text(timestamp, "green")
        colored_flag = self.color_text(flag, "cyan")
        log_type = self.color_text(level.value, self.get_color_for_level(level))

        log_message = f"{colored_timestamp} [{log_type}] {colored_flag}| {message}"
        
        try:
            if sys.stdout:
                sys.stdout.write(log_message + "\n")
                sys.stdout.flush()
            else:
                print(log_message)
        except Exception:
            # 最后的兜底：尝试用 ASCII 安全方式输出
            try:
                safe_msg = log_message.encode('utf-8', errors='replace').decode('utf-8')
                print(safe_msg)
            except Exception:
                pass

        if self.log_to_file:
            plain_message = f"{timestamp} [{level.value}] {flag}| {message}"
            try:
                with open(self.log_file_path, "a", encoding='utf-8') as f:
                    f.write(plain_message + "\n")
                    f.flush()
            except Exception:
                pass

    def get_color_for_level(self, level: LogLevel) -> str:
        """根据日志级别返回颜色"""
        level_colors = {
            LogLevel.INFO: "white",
            LogLevel.WARNING: "yellow",
            LogLevel.ERROR: "red",
            LogLevel.DEBUG: "cyan"
        }
        return level_colors.get(level, "white")

    def info(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.INFO, message, flag)

    def warning(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.WARNING, message, flag)

    def error(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.ERROR, message, flag)

    def debug(self, message: str, flag: str = "") -> None:
        self.log(LogLevel.DEBUG, message, flag)