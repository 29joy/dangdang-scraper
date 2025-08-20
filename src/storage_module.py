"""
storage_module.py
=================

This module encapsulates data storage operations for the DangDang book scraping project.
It handles directory creation, Excel file writing, and logging of image validation
and download failures.

Main functions:
1. `create_file`: Create necessary directories and log paths for output, images, and debug logs.
2. `save_info`: Save scraped data into Excel sheets per page, save failed image logs into JSON,
   and log the summary information.

本模块封装了当当图书爬虫项目的数据存储操作。
负责创建输出目录、写入 Excel 文件，并记录图片验证和下载失败日志。

主要功能：
1. `create_file`：创建 output、images 文件夹及各类日志路径。
2. `save_info`：将抓取数据分页保存到 Excel，失败图片信息写入 JSON 并记录日志。
"""

# ===== Standard Library Modules =====
from pathlib import Path

# ===== Third-Party Libraries =====
import pandas as pd

# ===== Custom Project Modules =====
from logger import logger, reconfigure_file_handler, log_to_json

def create_file():
    """
    Create project output directories and log file paths.

    Returns:
    - images_dir (Path): Directory to store downloaded images.
    - excel_path (Path): Path for saving Excel file.
    - run_log_path (Path): Path for run log.
    - img_not_valid_retry_log_path (Path): JSON log for retryable invalid images.
    - img_not_valid_unhandled_exception_log_path (Path): JSON log for unhandled exceptions during validation.
    - parsing_error_log_path (Path): JSON log for parsing errors.
    - img_validation_failures_log_path (Path): JSON log for images that failed validation.
    - download_img_failures_log_path (Path): JSON log for images that failed to download.
    """
    # Current file path (src/storage_module.py)
    current_file = Path(__file__).resolve()
    # Project root directory (parent of src)
    project_root = current_file.parent.parent
    # Output directories
    output_dir = project_root / 'output'
    images_dir = output_dir / 'images'
    excel_path = output_dir / 'dangdang_books.xlsx'
    images_dir.mkdir(parents=True, exist_ok=True)

    # Development and debug log directories
    dev_log_dir = project_root / "dev_logs"
    debug_log_dir = dev_log_dir / "debug_logs"
    debug_log_dir.mkdir(parents=True, exist_ok=True)

    # Configure context run log
    run_log_path = debug_log_dir / "run.log"
    reconfigure_file_handler(run_log_path)

    # Log paths
    img_not_valid_retry_log_path = debug_log_dir / "img_not_valid_retry.json"
    img_not_valid_unhandled_exception_log_path = debug_log_dir / "img_not_valid_unhandled_exception.json"
    parsing_error_log_path = debug_log_dir / "parsing_error.json"
    img_validation_failures_log_path = dev_log_dir / "img_validation_failures.json"
    download_img_failures_log_path = dev_log_dir / "download_img_failures.json"

    return (
        images_dir,
        excel_path,
        run_log_path,
        img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path,
        img_validation_failures_log_path,
        download_img_failures_log_path
    )

def save_info(all_pages_data, context):
    """
    Save scraped book data into Excel, and log failed images.

    - Each page's data is saved to a separate Excel sheet.
    - Second-download-failed images are saved into a 'failure summary' sheet.
    - Invalid image validation logs and second-download failures are written to JSON files.

    Parameters:
    - all_pages_data (list): List of page data, each page as a list of dictionaries.
    - context: Context object holding paths and fail lists.
    """
    # Save paginated data to Excel
    with pd.ExcelWriter(context.excel_path) as writer:
        for i, page_data in enumerate(all_pages_data, start=1):
            df = pd.DataFrame(page_data)
            df.to_excel(writer, sheet_name=f"Page {i}", index=False)

        # Save second-download failed images if any
        if len(context.second_download_fail_list):
            df_fail = pd.DataFrame(context.second_download_fail_list)
            df_fail.to_excel(writer, sheet_name="Failure Summary", index=False)

    # Log images that failed validation
    if len(context.img_validation_fail_list):
        for item in context.img_validation_fail_list:
            log_to_json(item, context.img_validation_failures_log_path)
        logger.info(
            f"{len(context.img_validation_fail_list)} images failed multiple validation attempts; logs saved to Excel and JSON."
        )
    else:
        logger.info("All images validated successfully, no failures.")

    # Log second-download failed images
    if len(context.second_download_fail_list):
        for item in context.second_download_fail_list:
            log_to_json(item, context.download_img_failures_log_path)
        logger.info(f"{len(context.second_download_fail_list)} images failed second download; logs saved to Excel and JSON.")
    else:
        logger.info("All images downloaded successfully, no failures.")
