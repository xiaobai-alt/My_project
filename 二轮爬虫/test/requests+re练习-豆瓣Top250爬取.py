import requests
import re

f = open('./top250.csv',mode='w',encoding='utf-8')
url = 'https://movie.douban.com/top250'


headers = {

'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}


response = requests.get(url,headers=headers).text



obj = re.compile(r'<div class="item">.*?<span class="title">(?P<Movie_name>.*?)</span>.*?<p class="">.*?'
                 r'导演:(?P<dao>.*?)&nbsp;.*?<br>'
                 r'(?P<time>.*?)&nbsp;.*?'
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                 r'<span>(?P<number>.*?)</span>',re.S) #re.S可以让正则中的.匹配换行符

result = obj.finditer(response)

for item in result:
    name = item.group('Movie_name')
    dao = item.group('dao')
    time = item.group('time').strip()  #strip用于去除字符串两边的空白
    score = item.group('score')
    number = item.group('number')
    f.write(f"{name},{dao},{time},{score},{number}\n")
f.close()





