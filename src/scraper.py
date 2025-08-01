"""
验证是否能正常req http
"""
import requests

url = "https://search.jd.com/Search?keyword=耳机"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    # User-Agent这个字段是告诉服务器：“我是一个什么样的客户端”
    # 默认情况下，Python requests 的 User-Agent 看起来不像“人类浏览器”，有的网站会拒绝返回内容
    # 举个例子，很多网站为了防爬虫，只有伪装成浏览器访问它，它才会返回正常内容
    # 这里就是告诉网站：“嘿，我是一个正常的浏览器，比如 Chrome。”
}

response = requests.get(url, headers=headers)
print(response.text[:1000])# 打印前1000个字符看看内容
