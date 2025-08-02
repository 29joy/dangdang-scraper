from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
driver = webdriver.Chrome(options=options)

# 访问搜索结果页
driver.get("https://search.dangdang.com/?key=人工智能&act=input")
time.sleep(5)    # 等待页面加载完毕

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
