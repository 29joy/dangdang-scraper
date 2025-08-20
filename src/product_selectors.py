"""
product_selectors.py
====================

This module defines the XPath and CSS selectors used for scraping product information
from DangDang search result pages. These selectors are referenced in the parse_module
to locate elements like title, price, author, image, and pagination buttons.

本模块定义了用于抓取当当网搜索结果页面商品信息的 XPath 和 CSS 选择器。
这些选择器在 parse_module 中被引用，用于定位标题、价格、作者、封面图以及翻页按钮等元素。
"""

SELECTORS = {
    "product_container": '//ul[@class="bigimg"]/li',        # Container for the product list
    "title": ".//a[@name='itemlist-title']",                # XPath for product title
    "price": 'search_now_price',                            # CSS class for product price
    "author": './/p[@class="search_book_author"]/span[1]',  # XPath for product author
    "image": 'img',                                         # Tag name for product image
    "next_page": "//li[@class='next']/a"                    # XPath for the next page button
}
