from bs4 import BeautifulSoup
import pandas as pd

# 读取保存好的 HTML 文件
with open("dangdang_ai.html", "r", encoding="utf-8") as f:
    html = f.read()

# 用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html, "lxml")

# 找到所有图书信息模块
# book_items = soup.find_all("li", class_="line1")
book_items = soup.select("ul.bigimg > li")    # 提取所有图书

# 用于保存所有图书信息的列表
books = []

for item in book_items:
    title = item.find("a", title=True).get("title").strip() if item.find("a", title=True) else "无标题"
    link = item.find("a", href=True).get("href") if item.find("a", href=True) else "无链接"
    author_tag = item.find("p", class_="search_book_author")
    author = author_tag.text.strip().split("\xa0\xa0")[0] if author_tag else "无作者"
    price_tag = item.find("span", class_="search_now_price")
    price = price_tag.text.strip() if price_tag else "无价格"

    books.append({
        "标题": title,
        "作者": author,
        "价格": price,
        "链接": link
    })

# 保存为 Excel 表格
df = pd.DataFrame(books)
df.to_excel("dangdang_books.xlsx", index=False, engine='openpyxl')

print("✅ 已成功保存为 dangdang_books.xlsx")
