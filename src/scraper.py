from bs4 import BeautifulSoup

# 读取保存好的 HTML 文件
with open("dangdang_ai.html", "r", encoding="utf-8") as f:
    html = f.read()

# 用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html, "lxml")

# 找到所有图书信息模块
# book_items = soup.find_all("li", class_="line1")    # class_="line1"只对应第一本书这样写只能提取到第一本书
book_items = soup.select("ul.bigimg > li")    # 提取所有图书

print("共找到图书数量：", len(book_items))

# 提取前10本书的信息
for i, item in enumerate(book_items[:10], start=1):
    # 标题
    title = item.find("a", title=True).get("title").strip() if item.find("a", title=True) else "无标题"

    # 链接
    link = item.find("a", href=True).get("href") if item.find("a", href=True) else "无链接"

    # 作者
    author_tag = item.find("p", class_="search_book_author")
    author = author_tag.text.strip().split("\xa0\xa0")[0] if author_tag else "无作者"

    # 价格
    price_tag = item.find("span", class_="search_now_price")
    price = price_tag.text.strip() if price_tag else "无价格"

    print(f"\n📘 第{i}本书：")
    print("标题：", title)
    print("作者：", author)
    print("价格：", price)
    print("链接：", link)
