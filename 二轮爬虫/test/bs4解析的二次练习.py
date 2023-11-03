# import requests
# from bs4 import BeautifulSoup

#用电影天堂为例
# url = 'https://www.dytt8.net/index2.htm'
#
#
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
#
# response = requests.get(url,headers=headers)
# response.encoding='gbk'
# page = response.text
#
# soup = BeautifulSoup(page,'lxml')
# test = soup.select('.co_content8 > ul')
# print(test)

#
# url = 'http://www.xinfadi.com.cn/index.html'
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
#
# response = requests.get(url,headers=headers).text
#
# soup = BeautifulSoup(response,'lxml')
# table = soup.select('.ul')
# print(table)

import requests
from bs4 import BeautifulSoup

url = 'https://www.umei.cc/meinvtupian/xingganmeinv/'

headers = {

'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
response = requests.get(url,headers=headers)
response.encoding='utf-8'
page = response.text

soup = BeautifulSoup(page,'lxml')
main_page_list = soup.select('.img >a>img')
print(main_page_list)
for i in main_page_list:
    src = i['data-original']
    page_name = i['alt'] +'.jpg'
    filename = './test/' + page_name
    response1 = requests.get(src,headers=headers).content
    with open(filename,mode='wb') as f:
        f.write(response1)
        print('保存成功')

































































