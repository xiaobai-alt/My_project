#获取简单百度页面保存本地
# import requests
#
# url = 'https://www.baidu.com'
#
# response = requests.get(url)
# response.encoding = 'utf-8'
# response_en = response.text
# print(response)
#
# with open('./baidu.html',encoding='utf-8',mode='w') as f:
#     f.write(response_en)


#带参数的搜狗搜索
# import requests
#
# url = "https://www.sogou.com/web"
# query = input("请输入要搜索的内容：\n")
# params = {
#     'query':query
# }
#
#
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
# response = requests.get(url,params=params,headers=headers).text
#
# with open('./搜索测试.html',mode='w',encoding='utf-8') as f:
#     f.write(response)

# import requests
# import json
# url = "https://fanyi.baidu.com/sug"
#
# kw = {
#     'kw':input('请输入要翻译的单词：\n')
# }
#
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
# response = requests.post(url,data=kw,headers=headers).json()
#
# print(response['data'])


#针对多参数get请求的ajex数据获取，以豆瓣网排行榜爱情片为例
# import requests
#
# url = 'https://movie.douban.com/j/chart/top_list'
#
# #对于多参数的get请求，将参数做成字典形式
# params = {
# 'type': '13',
# 'interval_id': '100:90' ,
# 'action':'' ,
# 'start': '0',
# 'limit': '20'
# }
#
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
# response = requests.get(url,params=params,headers=headers).json()
# print(response)

# import requests
# from lxml import etree
#
# url = 'https://live.photoplus.cn/live/pc/6359446#/live'
# headers = {
#
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# }
# # params = {
# # 'activityNo': '1551011',
# # 'isNew': 'false',
# # 'count': '500',
# # 'page': '1',
# # 'ppSign': 'live',
# # 'picUpIndex': '',
# # '_s': '0fe6a1931e209b989f02e365f46458d7',
# # '_t': '1677726049043'
# # }
# data = requests.post(url).json()
# print(data)

import requests
from lxml import etree

url = "http://www.glidedsky.com/login"


session = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
response = session.get(url,headers=headers).text
tree = etree.HTML(response)
token = tree.xpath('//div[@class="card-body"]/form/input/@value')[0]
#print(token)
data = {

	"_token": token,
	"email": "1946162355@qq.com",
	"password": "chenhao#include0"
}
response1 = session.post(url,data=data,headers=headers).text
tree1 = etree.HTML(response1)
test_url = tree1.xpath('/html/body/div/main/div[1]/div/div/table/tbody/tr/td[1]/a/@href')[0]
response2 = session.get(url=test_url,headers=headers).text
tree2 = etree.HTML(response2)
dow_url = 'http://www.glidedsky.com'+tree2.xpath('/html/body/div/main/div[1]/div/div/div/div/a/@href')[0]
response3 = session.get(dow_url,headers=headers).text
tree3 = etree.HTML(response3)
div_list = tree3.xpath('//div[@class="row"]/div')
numbers_list = []
for li in div_list:
	number = int(str(li.xpath('./text()')[0]).strip('\n'))
	numbers_list.append(number)
sum = 0
for i in range(0,len(numbers_list)):
	sum = sum + numbers_list[i]
print(sum)



# tree = etree.HTML(response)
# nub_list = tree.xpath('//div[@class="row"]/div')
# for li in nub_list:
#     number = li.xpath('./text()')
#     print(number)







