"""
parse_module.py
================

This module encapsulates the product parsing functionality.
- Extracts book information (title, price, author, cover image) from search result pages.
- Handles image downloading through the image_process module.
- Supports multi-pages crawling and error logging.
- Stores all parsed data in a structured list.

本模块封装了商品解析功能。
- 从搜索结果页面提取图书信息（标题、价格、作者、封面图）。
- 通过 image_process 模块处理封面图下载。
- 支持多页翻页抓取并记录解析错误。
- 将所有解析数据存储在结构化列表中。
"""

# ===== Standard Library Modules =====
import traceback

# ===== Third-Party Library Modules =====
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== Custom Project Modules =====
from product_selectors import SELECTORS
import image_process as img_pro
from logger import *


def parse_product(driver, context, config, selectors=None):
    """
    Parses product information from search result pages.

    Parameters:
        driver: Selenium WebDriver instance for browser interaction.
        context: Context object containing paths, logs, and temporary storage.
        config: Configuration dictionary (total pages, wait time, etc.).
        selectors: Optional dictionary of selectors; defaults to SELECTORS.

    Returns:
        List of lists, where each sublist contains product data dictionaries for one page.
        Each dictionary includes:
            - "Title"
            - "Price"
            - "Author"
            - "Cover_Img_Filename"
            - "Cover_Img_Path"
    """
    if selectors is None:
        selectors = SELECTORS

    # Create a container for storing all page data
    all_pages_data = []
    total_pages = config.get("total_pages")
    wait_time = config.get("wait_time")

    # Loop through pages
    for page in range(1, total_pages + 1):
        page_data = []
        logger.info(f"Scraping page {page}...")

        # Wait until all product containers are loaded
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.XPATH, selectors["product_container"]))
        )
        items = driver.find_elements(By.XPATH, selectors["product_container"])

        for idx, item in enumerate(items, start=1):
            try:
                # ===== Extract title, price, author, cover image URL =====
                title = item.find_element(By.XPATH, selectors["title"]).text.strip()
                price = item.find_element(By.CLASS_NAME, selectors["price"]).text.strip()
                author = item.find_element(By.XPATH, selectors["author"]).text.strip()
                img_el = item.find_element(By.TAG_NAME, selectors["image"])
                img_url = img_el.get_attribute('data-original') or img_el.get_attribute('src')

                # ===== Download cover image =====
                img_status, img_path = img_pro.process_image(img_url, title, price, author, page, idx, context)

                page_data.append({
                    "Title": title,
                    "Price": price,
                    "Author": author,
                    "Cover_Img_Filename": img_status,
                    "Cover_Img_Path": img_path
                })

            except Exception:
                error_msg = traceback.format_exc()
                logger.error(f"Failed to parse book {idx} on page {page}: {error_msg}")
                log_to_text(f"{datetime.now()} - Page {page} Book {idx}: {error_msg}\n", context.parsing_error_log_path)
                continue

        # Add current page data to overall data
        all_pages_data.append(page_data)

        # Navigate to next page
        if page < total_pages:
            try:
                next_button = driver.find_element(By.XPATH, selectors["next_page"])
                next_button.click()
            except Exception:
                logger.error("Next page button not found, ending pagination early.")
                break

    return all_pages_data
