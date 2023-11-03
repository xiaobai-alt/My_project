import requests
from lxml import etree
from chaojiying import Chaojiying_Client as cj

#需求：对马蜂窝网进行模拟登陆，并获取个人信息对应页面数据
"""
1.先对马蜂窝网登录页面进行分析：
    --页面会在账户输入，密码为空的情况下弹出验证码框，此处直接分析页面，进行验证码的地址获取存贮与识别
2.对马蜂窝网进行post模拟登陆
3.对个人页面对应页面数据进行获取保存
"""
#创建session对象
session = requests.Session()

#创建验证码识别方法
def getCode(imgPath,codeType):
    result = 'None'
    if __name__ == '__main__':
        chaojiying = cj('Mrchen123', 'chenhao#include0', '942032')  # 用户中心>>软件ID 生成一个替换 96001
        im = open(imgPath, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        result = chaojiying.PostPic(im, codeType)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        # print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码
    return result
#验证码的获取与识别
login_url = "https://passport.mafengwo.cn/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

login_page_text = session.get(url=login_url,headers=headers).text
tree = etree.HTML(login_page_text)
code_src = 'https://passport.mafengwo.cn' + tree.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/form/div[3]/a/img/@src')[0]

#对验证码图片进行获取保存
code_data = session.get(url=code_src,headers=headers).content
with open('./马蜂窝.jpg','wb') as fp:
    fp.write(code_data)

#对验证码进行识别
code_text = getCode('马蜂窝.jpg',1004)
print('识别结果为：',code_text.get('pic_str'))
code = code_text.get('pic_str')

data = {
	"passport": "eyJjb250ZW50IjoibjFZejNkRndnWW8xNkNBNUhCSzZCQ3RLRTZjdEZpWkdkM1I1aytkNlVlaz0iLCJrZXkiOiJJTGZKblJ3RGVzVGwxL29VaXZRLzFna3ZMSitMVTNUaHlJWlFMTFBiQmc3M3VsMVl6ek01NlI2VUY4T2pkNXZhRHNhMUxRQWEzUmp5QmxPK2JpMkV4VzlLb01nT0dxU3hLTmJtTFlQd0VzN0pCelBTTm5BaXE1YUI5MzdYd3llRkUvYmxFWUx0WVN1OHpyZzFMWVFtcWxWczFyUm5rTkxsVDRHOEZJalMwMHBpdU5jUElOMUhDR0QyTWxmc2QyeGVLRmFTMks0djMxMGhJaTBrQnl2U3VQMDVSUnU2OU5jc0J5VTJZRzE3RTVLOVV2Tlora0VmSW50YWtuSHBlRWpTdWd4KzR4OFRwelFVcFd3RlJ0WHFiby9IZVE0dHkydkZNTFJMRTNnejE4bXR3eHBTaUxzM2Z6Y05FakFNaUgwZHZHZEhkbnZTVXlJSEdIRkRmUGRvYWc9PSIsInZlciI6MX0=",
	"password": "eyJjb250ZW50IjoiakkwaEoxODRnL1l5WWNjdksrUHk2dUYwRlZUQWJHUzdodlI1Rk9tUGR5QT0iLCJrZXkiOiJmR01uTE1TQlZBVkg1dmxZQUVUcjZFRDFBWUozcEZrZkhJSlhoZGtxd01sR2gwWFUxMHZIZC9VMG5JSHByM0pZQkFWSlRCN1Z2emRYQkt3RWUxbTg5LzJaRUQ4TkxWMERzY0x1aTE1K0FraWV0aHdiaUljSmdNZ3o5djNpbHVUVjk1anNmaTk2YlVBdTgxRWFwbFRmK3dNME5wUkQvYVgvRFR1bWZSaW5JL3EwVU04aEEyTzFHNVFDRGx0dTBnTHJGQUdRUDJYQytQdFVOMFhiRElOZkhKYVN6QUJ6RWhvR0FmcmVFVU15SDJPM2NpWmJhbCt1S0lwM0JhSmRYOUZSNk5UaURsUHhmMmJmUit6QWdQRGM3dFpZcERSOHU0Y3JweWh5dElmdCtsVGlEK0JZaldzVHJSL25QVnZ6dUdodjY3ek9MZTRxTTU0UEZ5SXNZamh6Y3c9PSIsInZlciI6MX0=",
	"code": code
}

#采用session进行post请求
response = session.post(url=login_url,headers=headers,data=data)
#输出状态码查看是否请求成功
print(response.status_code)

detail_url = 'https://www.mafengwo.cn/u/78048951.html'
detail_page_text = session.get(url=detail_url,headers=headers).text
with open('./马蜂窝.html','w',encoding='utf-8') as fp:
    fp.write(detail_page_text)
print('Over')