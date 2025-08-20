"""
context.py

Module Description:
This module defines the Context dataclass for storing paths and runtime state information
during the scraping process. It centralizes all file paths, logging paths, and failure lists
so that different modules can access and update shared runtime data consistently.

A helper function `create_context` is provided to initialize the Context object with proper
paths obtained from the storage module.

模块说明：
该模块定义了 Context 数据类，用于在爬取过程中存储路径和运行时状态信息。
它集中管理所有文件路径、日志路径及失败列表，使不同模块能够一致地访问和更新共享运行数据。

提供了辅助函数 `create_context` 来使用 storage_module 提供的路径初始化 Context 对象。
"""

from dataclasses import dataclass
from typing import List
from pathlib import Path
import storage_module as sto_m


@dataclass
class Context:
    """Dataclass to store paths and runtime state during scraping.

    Attributes:
        images_dir: Path to the images output directory.
        excel_path: Path to the Excel file to save product data.
        logger_path: Path to the current log file.
        img_not_valid_retry_log_path: Path to log images failed but retried.
        img_not_valid_unhandled_exception_log_path: Path to log images with unhandled exceptions.
        parsing_error_log_path: Path to log parsing errors.
        img_validation_failures_log_path: Path to log images that failed validation multiple times.
        download_img_failures_log_path: Path to log images that failed downloading multiple times.
        img_validation_fail_list: List of items failed during image validation.
        first_download_fail_list: List of items that failed during the first download attempt.
        second_download_fail_list: List of items that failed during the second download attempt.
    """
    images_dir: Path
    excel_path: Path
    logger_path: Path
    img_not_valid_retry_log_path: Path
    img_not_valid_unhandled_exception_log_path: Path
    parsing_error_log_path: Path
    img_validation_failures_log_path: Path
    download_img_failures_log_path: Path
    img_validation_fail_list: List
    first_download_fail_list: List
    second_download_fail_list: List


def create_context() -> Context:
    """
    Factory function to initialize and return a Context object with proper paths.

    Returns:
        Context: Initialized context object with paths and empty failure lists.
    """
    (
        images_dir, excel_path, logger_path,
        img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path,
        img_validation_failures_log_path,
        download_img_failures_log_path
    ) = sto_m.create_file()

    return Context(
        images_dir=images_dir,
        excel_path=excel_path,
        logger_path=logger_path,
        img_not_valid_retry_log_path=img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path=img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path=parsing_error_log_path,
        img_validation_failures_log_path=img_validation_failures_log_path,
        download_img_failures_log_path=download_img_failures_log_path,
        img_validation_fail_list=[],
        first_download_fail_list=[],
        second_download_fail_list=[]
    )
