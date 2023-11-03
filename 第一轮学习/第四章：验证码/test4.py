# !/usr/bin/env python
# coding:utf-8
import requests
from lxml import etree
from hashlib import md5

from chaojiying import Chaojiying_Client

url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    }
page_text = requests.get(url=url,headers=headers).text
tree = etree.HTML(page_text)
code_img_src = "https://so.gushiwen.cn" + tree.xpath('//*[@id="imgCode"]/@src')[0]
img_data = requests.get(url=code_img_src,headers=headers).content
with open('./code.jpg','wb') as fp:
    fp.write(img_data)
#调用chaojiying函数的功能
Cj = Chaojiying_Client('Mrchen123', 'chenhao#include0', '942032')
code_text = Cj.PostPic('code.jpg',1902)

print('识别结果为：',code_text)