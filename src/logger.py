"""
logger.py
==========

This module provides logging utilities for the project, including:
- Global logger with console and file handlers
- Size and time-based rotating file handler
- Context-specific logger for per-run log files
- JSON and text log helper functions

本模块提供项目日志功能，包括：
- 全局日志（控制台 + 文件）
- 按大小和时间轮转的日志处理器
- Context 专属日志（每次运行独立日志文件）
- JSON 和文本日志写入辅助函数
"""

from pathlib import Path
import logging
import os
import json
import re
import time
import glob
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# ================= Global log path =================
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # Project root directory
log_dir = project_root / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
GLOBAL_LOG_PATH = log_dir / "run_log.log"


class SizeAndTimeRotatingFileHandler(TimedRotatingFileHandler):
    """
    Log handler that rotates by date and size.
    - Generates a new file at midnight every day.
    - Rolls over when file exceeds maxBytes.
    - Keeps logs of last 'backupDays' days.

    按日期 + 大小轮转的日志处理器。
    - 每天零点生成新文件
    - 文件超过 maxBytes 时分卷
    - 只保留最近 backupDays 天的日志文件
    """

    def __init__(self, filename, when='midnight', interval=1,
                 backupDays=7, maxBytes=5*1024*1024, encoding="utf-8"):
        self.maxBytes = maxBytes
        self.backupDays = backupDays
        super().__init__(filename, when, interval, backupCount=0, encoding=encoding)

    def shouldRollover(self, record):
        """Check if rollover is needed based on size or time."""
        if super().shouldRollover(record):
            return 1
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = f"{self.format(record)}\n"
            if self.stream.tell() + len(msg.encode(self.encoding or "utf-8")) >= self.maxBytes:
                return 1
        return 0

    def doRollover(self):
        """Perform rollover and clean old logs."""
        super().doRollover()
        self.clean_old_logs()

    def clean_old_logs(self):
        """Delete log files older than backupDays."""
        log_dir, base_filename = os.path.split(self.baseFilename)
        pattern = os.path.join(log_dir, f"{base_filename}*")

        cutoff = time.time() - (self.backupDays * 86400)
        for logfile in glob.glob(pattern):
            match = re.search(r"\.(\d{4}-\d{2}-\d{2})", logfile)
            if match:
                try:
                    file_time = time.mktime(time.strptime(match.group(1), "%Y-%m-%d"))
                    if file_time < cutoff:
                        os.remove(logfile)
                        print(f"[Log Cleanup] Deleted old log: {logfile}")
                except Exception as e:
                    print(f"[Log Cleanup Error] {e}")


# ================= Logger configuration =================
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# --------- Global log handler (append mode) ---------
if not logger.handlers:
    global_file_handler = SizeAndTimeRotatingFileHandler(
        filename=GLOBAL_LOG_PATH,
        when="midnight",
        interval=1,
        backupDays=7,
        maxBytes=5 * 1024 * 1024,
        encoding="utf-8"
    )
    global_file_handler.setFormatter(formatter)
    logger.addHandler(global_file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Context-specific log handler (can be switched dynamically)
context_file_handler = None


def reconfigure_file_handler(context_log_path: Path):
    """
    Enable a context-specific log file.
    - Creates a new log file each call (overwrite mode)
    - Works together with the global logger

    启用 Context 专属日志文件
    - 每次调用都会新建一个日志文件（覆盖模式）
    - 与全局日志同时生效
    """
    global context_file_handler

    if context_file_handler:
        logger.removeHandler(context_file_handler)

    Path(context_log_path).parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(context_log_path, mode="w", encoding="utf-8")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    context_file_handler = handler

    logger.info(" ====== Context log separator ======")
    logger.info(f"Context log switched to: {context_log_path}")


# ---------------- Helper functions ----------------
def log_to_json(data: dict, file_path: Path):
    """Write a JSON log entry (append mode)."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}]\n")
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")
        logger.info(f"JSON log written: {file_path} | {data}")
    except Exception as e:
        logger.error(f"Failed to write JSON log: {e} | data={data}")


def log_to_text(message: str, file_path: Path):
    """Write a text log entry (append mode)."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
        logger.info(f"Text log written: {file_path} | {message}")
    except Exception as e:
        logger.error(f"Failed to write text log: {e} | message={message}")
