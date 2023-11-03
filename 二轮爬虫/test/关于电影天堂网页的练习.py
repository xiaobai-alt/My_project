import requests
import re

#实验目的：获取主页面的电影链接地址
url = "https://www.dytt8.net/index2.htm"
response = requests.get(url)
response.encoding='gbk'
result = response.text


obj = re.compile(r"2023新片精品.*?<ul>(?P<html>.*?)</ul>",re.S)
result1 = obj.search(result)
html = result1.group("html")

obj2 = re.compile(r"最新电影下载</a>]<a href=(?P<movie_url>.*?)(?P<movie_name>.*?)</a>")
result2 = obj2.finditer(html)

for item in result2:
    movie_url = item.group('movie_url')
    movie_name = item.group('movie_name')







































































