from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import openpyxl

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

# 抓取所有商品信息
books = driver.find_elements(By.XPATH, '//ul[@class="bigimg"]/li')
print(f"共找到 {len(books)} 本书")

book_list = []
for book in books:
    try:
        title = book.find_element(By.XPATH, './/a[@name="itemlist-title"]').text.strip()
        author = book.find_element(By.XPATH, './/p[@class="search_book_author"]/span[1]').text.strip()
        price = book.find_element(By.XPATH, './/span[@class="search_now_price"]').text.strip()
        book_list.append([title, author, price])
    except Exception as e:
        continue

driver.quit()

# 保存为 Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['标题', '作者', '价格'])
for book in book_list:
    ws.append(book)

wb.save("dangdang_books.xlsx")
print("✅ 已成功保存为 dangdang_books.xlsx")
