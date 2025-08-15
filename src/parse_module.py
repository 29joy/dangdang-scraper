# 解析功能封装
# ===== 标准库模块 =====
import time
import traceback
from datetime import datetime

# ===== 第三方库 =====
from selenium.webdriver.common.by import By

# ===== 项目自定义模块 =====
# from mymodule import myfunction
import image_process as img_pro


def get_product_info(book):
    # ===== 获取标题 =====
    title = book.find_element(By.XPATH, './/a[@name="itemlist-title"]').text.strip()

    # ===== 获取价格 =====
    price = book.find_element(By.CLASS_NAME, "search_now_price").text.strip()

    # ===== 获取作者 =====
    author = book.find_element(
        By.XPATH, './/p[@class="search_book_author"]/span[1]'
    ).text.strip()

    # ===== 进入封面图片下载流程 =====
    img_el = book.find_element(By.TAG_NAME, "img")
    # img download阶段1: 从HTML中获取图片URL
    img_url = img_el.get_attribute("data-original") or img_el.get_attribute("src")

    return title, price, author, img_url


def parse_product(driver, context):
    # 创建数据存储容器
    all_pages_data = []  # 每一页是一个列表
    total_pages = 3
    img_validation_fail_list = []

    # 循环实现翻页功能
    for page in range(1, total_pages + 1):
        page_data = []
        print(f"正在抓取第 {page} 页...")

        time.sleep(3)  # 等待页面加载
        # ===== 定位图书 =====
        books = driver.find_elements(By.XPATH, '//ul[@class="bigimg"]/li')

        for idx, book in enumerate(books, start=1):
            try:
                # ===== 获取标题、价格、作者、封面图URL =====
                title, price, author, img_url = get_product_info(book)
                # ===== 封面图下载 =====
                img_status, img_path = img_pro.process_image(
                    img_url,
                    title,
                    price,
                    author,
                    page,
                    idx,
                    img_validation_fail_list,
                    context,
                )
                page_data.append(
                    {
                        "标题": title,
                        "价格": price,
                        "作者": author,
                        "封面图文件名": img_status,
                        "封面图路径": img_path,
                    }
                )
            except Exception:
                error_msg = traceback.format_exc()
                print(f"[Error] 第{page}页第{idx}本书解析失败: {error_msg}")
                with open(context.parsing_error_log_path, "a", encoding="utf-8") as log:
                    log.write(f"{datetime.now()} - 第{page}页第{idx}本: {error_msg}\n")
                continue

        # 当前页数据加入总数据
        all_pages_data.append(page_data)

        # 翻页
        if page < total_pages:
            try:
                next_button = driver.find_element(By.LINK_TEXT, "下一页")
                driver.execute_script("arguments[0].click();", next_button)
            except:
                print("找不到‘下一页’，提前结束")
                break
    return all_pages_data, img_validation_fail_list
