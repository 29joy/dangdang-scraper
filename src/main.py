"""
main.py
=========

This is the main pipeline controller for the project.
- Creates necessary folders and files
- Opens the browser to the search page
- Parses product information
- Handles image downloading (including retry for failed downloads)
- Saves extracted data
- Logs the entire process

主流程控制文件
- 创建必要的文件夹和文件路径
- 打开浏览器访问搜索页面
- 解析产品信息
- 图片下载及失败图片二次下载处理
- 保存抓取到的数据
- 记录整个流程日志
"""

# ===== Standard Library Modules =====

# ===== Third-Party Library Modules =====

# ===== Custom Project Modules =====
import context as ctx_mod
import request_module as req_m
import parse_module as parse_m
import image_process as img_pro
import storage_module as sto_m
from logger import logger
from config import *


def run_pipeline(
        keyword: str,
        target_website: str,
):
    """
    Main pipeline execution function.

    Steps:
    1. Create folders and file paths
    2. Open the browser and navigate to search page
    3. Parse product information
    4. Retry downloading failed images
    5. Save extracted data
    6. Log completion

    主流程执行函数。

    步骤：
    1. 创建文件夹和文件路径
    2. 打开浏览器并访问搜索页面
    3. 解析产品信息
    4. 对下载失败的图片进行二次下载
    5. 保存抓取到的数据
    6. 记录完成日志
    """
    # ===== Create folders and file paths =====
    context = ctx_mod.create_context()

    # ===== Open browser and navigate to search page =====
    driver = req_m.open_search_page(keyword, target_website, PARSE_PRODUCT_CONFIG)
    try:
        # ===== Enter main data acquisition flow =====
        all_pages_data = parse_m.parse_product(driver, context, PARSE_PRODUCT_CONFIG, selectors=None)

        # ===== Retry downloading failed images =====
        img_pro.final_download_for_fail_img(all_pages_data, context, IMAGE_DOWNLOAD_CONFIG)
    finally:
        # ===== Close browser =====
        req_m.driver_quit(driver)

    # ===== Save extracted data and information =====
    sto_m.save_info(all_pages_data, context)

    # ===== Log pipeline completion =====
    logger.info("Data scraping and saving completed.")


if __name__ == "__main__":
    # Default parameters for local execution
    run_pipeline(
        keyword="AI",
        target_website='https://www.dangdang.com/'
    )
