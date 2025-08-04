from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import requests

def download_image(img_url, save_path):
    try:
        if img_url.startswith("//"):
            img_url = "http:" + img_url
        elif img_url.startswith("/"):
            img_url = "https://www.dangdang.com" + img_url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(img_url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download image: {img_url} ({response.status_code})")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

# 初始化浏览器
options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

# 搜索关键词
keyword = 'AI'
driver.get('https://www.dangdang.com/')
time.sleep(2)    # 等待页面加载完毕

# 输入搜索内容并回车
search_input = driver.find_element(By.ID, 'key_S')    # 定位搜索框
search_input.send_keys(keyword)    # 输出关键词
search_input.send_keys(Keys.ENTER)    # 点击回车进行搜索
time.sleep(3)    # 等待页面加载完毕

# ------------------------------------分页存储--------------------------------
# 创建数据存储容器
all_pages_data = []  # 每一页是一个列表
total_pages = 3

# 图片保存文件夹
os.makedirs('./output/images', exist_ok=True)

for page in range(1, total_pages + 1):
    print(f"正在抓取第 {page} 页...")

    time.sleep(3)  # 等待页面加载
    books = driver.find_elements(By.XPATH, '//ul[@class="bigimg"]/li')

    page_data = []

    for idx, book in enumerate(books, start=1):
        try:
            title = book.find_element(By.XPATH, './/a[@name="itemlist-title"]').text.strip()
            price = book.find_element(By.CLASS_NAME, 'search_now_price').text.strip()
            author = book.find_element(By.XPATH, './/p[@class="search_book_author"]/span[1]').text.strip()
            img_el = book.find_element(By.TAG_NAME, 'img')
            img_url = img_el.get_attribute('data-original') or img_el.get_attribute('src')

            if img_url:
                img_filename = f"page{page}_book{idx}.jpg"
                img_path = os.path.join(r'output\images', img_filename)
                # 下载封面图
                download_image(img_url, img_path)
            else:
                img_path = "无图片"

            page_data.append({
                "标题": title,
                "价格": price,
                "作者": author,
                "封面图文件名": os.path.basename(img_path),
                "封面图路径": img_path
            })
        except Exception as e:
            print(f"错误：{e}")
            continue

    # 当前页数据加入总数据
    all_pages_data.append(page_data)

    # 翻页
    if page < total_pages:
        try:
            next_button = driver.find_element(By.LINK_TEXT, '下一页')
            driver.execute_script("arguments[0].click();", next_button)
        except:
            print("找不到‘下一页’，提前结束")
            break

# 关闭浏览器
driver.quit()

# 分页存入 Excel
with pd.ExcelWriter('dangdang_books.xlsx') as writer:
    for i, page_data in enumerate(all_pages_data, start=1):
        df = pd.DataFrame(page_data)
        df.to_excel(writer, sheet_name=f"第{i}页", index=False)

print("抓取与保存完成。")
