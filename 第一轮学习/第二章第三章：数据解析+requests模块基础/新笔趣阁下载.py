import requests
from lxml import etree
import time

session = requests.Session()
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}
index_url = 'http://www.biqu5200.net/'
page_text = session.get(url=index_url,headers=headers).text
tree = etree.HTML(page_text)

list_1 = tree.xpath('//div[@class="nav"]/ul/li')
#小说分类列表
variety_dict = {}
for li in list_1:
    """
    'variety_name':小说种类名
    'variety_href'：不同种类网址
    """
    variety_name = li.xpath('./a/text()')[0]
    variety_href = 'https:' + li.xpath('./a/@href')[0]
    #将获取到的小说分类加载到分类列表
    variety_dict[variety_name] = variety_href
print(variety_dict.keys())
print('请选择想要获取的小说种类：\n')
chose_variety = str(input())
#print(variety_dict.get(chose_variety))
page_url = variety_dict.get(chose_variety)

variety_page_text = session.get(url=page_url,headers=headers).text
tree1 = etree.HTML(variety_page_text)

list_variety = tree1.xpath('//div[@class="l"]/ul/li')

list_variety_dict = {}
for li in list_variety:
    note_name = li.xpath('./span[@class="s2"]/a/text()')[0]
    note_url = li.xpath('./span[@class="s2"]/a/@href')[0]
    list_variety_dict[note_name] = note_url
print(list_variety_dict)




