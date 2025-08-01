"""
将http保存到本地，方便初期反复调试，避免频繁刷新或req http触发反爬或强制登录等
"""
from selenium import webdriver
import time

# 打开浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 不显示浏览器界面，可选
driver = webdriver.Chrome(options=options)

# 打开当当搜索页面（以“人工智能”为例）
driver.get("https://search.dangdang.com/?key=人工智能&act=input")

# 等待页面加载（时间可视网速调整）
time.sleep(5)

# 保存当前渲染后的页面源码
with open("dangdang_ai.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("已保存完整渲染后的 HTML 文件")
