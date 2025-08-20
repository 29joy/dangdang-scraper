"""
request_module.py
=================

This module encapsulates browser operations using Selenium to open DangDang search
pages, input search keywords, wait for the results to load, and handle browser closure.

It provides:
1. `open_search_page`: Open the target website, input a keyword, wait for the product list to load.
2. `driver_quit`: Safely quit the Selenium WebDriver session.

本模块封装了使用 Selenium 的浏览器操作，用于打开当当搜索页面、输入搜索关键词、
等待搜索结果加载，并处理浏览器关闭。

提供的功能：
1. `open_search_page`：打开目标网站，输入搜索关键词，并等待商品列表加载完成。
2. `driver_quit`：安全退出 Selenium WebDriver 会话。
"""

# ===== Standard Library Modules =====

# ===== Third-Party Libraries =====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product_selectors import SELECTORS

# ===== Custom Project Modules =====

def open_search_page(keyword: str, target_website: str, config: dict, selectors: dict = None) -> webdriver.Chrome:
    """
    Open the search page on DangDang and input the search keyword.

    Parameters:
    - keyword (str): The keyword to search for.
    - target_website (str): The base URL of the website.
    - config (dict): Configuration dictionary with 'wait_time' key.
    - selectors (dict, optional): Dictionary of selectors for locating elements.

    Returns:
    - driver (webdriver.Chrome): Selenium Chrome WebDriver instance with the search results loaded.
    """
    wait_time = config.get("wait_time")
    if selectors is None:
        selectors = SELECTORS

    # Initialize Chrome browser
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    # Navigate to the target website
    driver.get(target_website)

    # Wait for the search input box to appear (ensure page is loaded)
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.ID, 'key_S'))
    )

    # Input the search keyword and press Enter
    search_input = driver.find_element(By.ID, 'key_S')  # Locate search box
    search_input.send_keys(keyword)                     # Enter keyword
    search_input.send_keys(Keys.ENTER)                 # Press Enter to search

    # Wait until product containers appear in the search results
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_all_elements_located((By.XPATH, selectors["product_container"]))
    )

    return driver

def driver_quit(driver: webdriver.Chrome) -> None:
    """
    Quit the Selenium WebDriver session safely.

    Parameters:
    - driver (webdriver.Chrome): The Selenium WebDriver instance to quit.
    """
    driver.quit()
