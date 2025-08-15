# 请求功能封装
# ===== 标准库模块 =====
import time

# ===== 第三方库 =====
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ===== 项目自定义模块 =====
# from mymodule import myfunction


# 浏览器操作获取搜索图书页面
def open_search_page(keyword, target_website):
    # 初始化浏览器
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # 搜索关键词
    # keyword = 'AI'
    driver.get(target_website)
    time.sleep(2)  # 等待页面加载完毕

    # 输入搜索内容并回车
    search_input = driver.find_element(By.ID, "key_S")  # 定位搜索框
    search_input.send_keys(keyword)  # 输出关键词
    search_input.send_keys(Keys.ENTER)  # 点击回车进行搜索
    time.sleep(3)  # 等待页面加载完毕

    return driver


# 关闭浏览器
def driver_quit(driver):
    driver.quit()
