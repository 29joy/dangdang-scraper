# ===== 标准库模块 =====
from pathlib import Path
import os
import time

# ===== 第三方库 =====
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ===== 项目自定义模块 =====
# from mymodule import myfunction

# 当前文件的路径（src/scraper.py）
current_file = Path(__file__).resolve()
# 项目根目录（即 src 的上一级）
project_root = current_file.parent.parent
# 输出文件夹：output（在项目根目录下）
output_dir = project_root / 'output'
images_dir = output_dir / 'images'
excel_path = output_dir / 'dangdang_books.xlsx'
# 创建 output 和 images 文件夹
images_dir.mkdir(parents=True, exist_ok=True)

min_image_file_size = 2048

# is_valid_image_url 判断img URL是否有效
def is_valid_image_url(img_url: str) -> bool:

    return True

# is_valid_image 判断img是否有效
def is_valid_image(img_url, max_retries=3):
    # img download阶段2：标准化URL(补全http/https等)
    if img_url.startswith("//"):
        img_url = "http:" + img_url
    elif img_url.startswith("/"):
        img_url = "https://www.dangdang.com" + img_url

    # img download阶段阶段 3：初步 URL 判断
    # 阶段3.1: 是否是空链接、错误路径、伪链接(如 /images/none.jpg)
    if not img_url:
        return False, img_url
    if img_url.strip() in ["", "#"]:
        return False, img_url
    if "none.jpg" in img_url or "default.png" in img_url:
        return False, img_url
    # 阶段3.2: 先基于URL判断明显无效图
    if 'nofound_o.jpg' in img_url:
        return False, img_url

    # img download阶段4: 发送请求(请求本身的网络层问题)
    # # 阶段4.0: 设置网络请求配置->后续主内容移出到config.py配置项文件
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.dangdang.com'
    }
    try:
        # 阶段4.1: 配置Session和重试机制防止偶发网络错误
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=1,  # 等待时间：1s, 2s, 4s...
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(img_url, headers=headers, timeout=15)
        # 阶段4.2: 检查响应是否成功
        if response.status_code == 200:    # 响应成功
            # img download阶段5：响应内容校验
            # 阶段5.1：过滤掉伪装成图片的网页、JSON、JS等内容
            content_type = response.headers.get('Content-Type', '')
            if content_type in ['image/jpeg', 'image/png', 'image/webp']:    # 正确图片, 保存逻辑
                # 阶段5.2：response.url是否跳转到了占位图
                if 'nofound_o.jpg' in response.url:
                    return False, img_url
                # 阶段5.3：内容长度小于设定值说明是空图、错误图片或加载不全
                if len(response.content) > min_image_file_size:
                    return True, img_url
                else:
                    return False, img_url
            else:    # 记录失败日志
                print(f"跳过非图片链接: {img_url}，类型: {content_type}")
        else:
            return False, img_url    # 增加reason为响应失败

    except Exception as e:
        print(f"[is_valid_image] Error {img_url}: {e}")
        return False, img_url

# 接收清洗过的URL下载图片
def download_image(img_url, save_path, max_retries=3):
    try:
        # 配置 Session 和重试机制
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=1,  # 等待时间：1s, 2s, 4s...
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(img_url, timeout=5)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading{save_path}, {img_url}: {e}")    # 加了save_path帮助验证是哪张图片
        return False

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
first_fail_list = []
second_fail_list = []

# 图片保存文件夹
os.makedirs('./output/images', exist_ok=True)

for page in range(1, total_pages + 1):
    page_data = []
    print(f"正在抓取第 {page} 页...")

    time.sleep(3)  # 等待页面加载
    books = driver.find_elements(By.XPATH, '//ul[@class="bigimg"]/li')

    for idx, book in enumerate(books, start=1):
        try:
            title = book.find_element(By.XPATH, './/a[@name="itemlist-title"]').text.strip()
            price = book.find_element(By.CLASS_NAME, 'search_now_price').text.strip()
            author = book.find_element(By.XPATH, './/p[@class="search_book_author"]/span[1]').text.strip()
            img_el = book.find_element(By.TAG_NAME, 'img')
            # img download阶段1: 从HTML中获取图片URL
            img_url = img_el.get_attribute('data-original') or img_el.get_attribute('src')

            is_valid, new_img_url = is_valid_image(img_url)
            img_filename = f"page{page}_book{idx}.jpg"
            img_path = images_dir / img_filename    # 验证无图片的情况，可能改回去
            if is_valid:
                # img_filename = f"page{page}_book{idx}.jpg"
                # img_path = images_dir / img_filename
                success = download_image(new_img_url, img_path)
                if success:
                    img_status = os.path.basename(img_path)
                else:
                    print("图片下载失败，即将加入first_fail_list")
                    img_status = "下载失败"  # 加入下载状态变量
                    first_fail_list.append({
                        "标题": title,
                        "价格": price,
                        "作者": author,
                        "封面图链接": new_img_url,
                        "封面图路径": img_path
                    })  # 下载失败的图片加入first_fail_list
                    img_path = "无图片"
            else:
                print(f"{img_path}{new_img_url}第一次下载失败，进入无图片或占位图")
                img_status = "无图片或占位图"
                img_path = "无图片"

            page_data.append({
                "标题": title,
                "价格": price,
                "作者": author,
                "封面图文件名": img_status,
                "封面图路径": img_path
            })
        except Exception as e:
            print(f"[Error] {e}")
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

# 二次下载图片
if len(first_fail_list):
    print("开始图片二次下载")
    for item in first_fail_list:
        success = download_image(item["封面图链接"], item["封面图路径"])
        if success:
            img_status = os.path.basename(item["封面图路径"])
            # 定位到对应的位置，更改封面图文件名和封面图路径
            # 如果用all_pages_data就要在保存进Excel之前，或者可以在这里打开'dangdang_books.xlsx'再操作，这里先用all_pages_data来操作
            for page_data in all_pages_data:
                for entry in page_data:
                    if entry["标题"] == item["标题"]:
                        entry["封面图文件名"] = img_status
                        entry["封面图路径"] = item["封面图路径"]
                        break
        else:
            print(f"{item["封面图链接"]}图片二次下载失败，即将存入失败汇总页")
            second_fail_list.append({
                "标题": item["标题"],
                "价格": item["价格"],
                "作者": item["作者"],
                "封面图文件名": os.path.basename(item["封面图路径"]),
                "封面图路径": item["封面图路径"]
            })  # 下载失败的图片加入second_fail_list

# 关闭浏览器
driver.quit()

# 分页存入 Excel
with pd.ExcelWriter(excel_path) as writer:
    for i, page_data in enumerate(all_pages_data, start=1):
        df = pd.DataFrame(page_data)
        df.to_excel(writer, sheet_name=f"第{i}页", index=False)

        # 判断是否存在second_fail_list需要保存，存在即保存
        if len(second_fail_list):
            df_fail = pd.DataFrame(second_fail_list)
            df_fail.to_excel(writer, sheet_name=f"失败汇总页", index=False)

print("抓取与保存完成。")
