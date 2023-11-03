import requests
from lxml import etree
from chaojiying import Chaojiying_Client as cj
def getCode(imgPath,codeType):
    result = 'None'
    if __name__ == '__main__':
        chaojiying = cj('Mrchen123', 'chenhao#include0', '942032')  # 用户中心>>软件ID 生成一个替换 96001
        im = open(imgPath, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        result = chaojiying.PostPic(im, codeType)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        # print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码
    return result
#创建一个session对象
session = requests.Session()

#对进行模拟登陆
url = 'https://www.chaojiying.com/user/login/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    }
page_text = session.get(url=url,headers=headers).text

tree = etree.HTML(page_text)
code_img_src = 'https://www.chaojiying.com' + tree.xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img/@src')[0]

code_img_data = session.get(url=code_img_src,headers=headers).content
with open('./code.jpg','wb') as fp:
    fp.write(code_img_data)
#使用超级鹰提供的示例代码对验证码图片进行识别
code_text = getCode('code.jpg',1004)
print('识别结果为：',code_text.get('pic_str'))
code = code_text.get('pic_str')

login_url = 'https://www.chaojiying.com/user/login/'
data = {
        "user": "Mrchen123",
        "pass": "chenhao#include0",
        "imgtxt": code,
        "act": "1"

}
#响应码可以用来判断是否成功
#使用session进行post请求
response = session.post(url=login_url,headers=headers,data=data)
print(response.status_code)

#爬取当前个人用户中心主页对应的页面数据
detail_url = "https://www.chaojiying.com/user/"

#手动cookie处理，不建议使用
"""
headers = {
    'Cookie':'PHPSESSID=lm8253c2fds3pp6232mripdhkn; __tins__16851773=%7B%22sid%22%3A%201669641156636%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201669642956636%7D; __51cke__=; __51laig__=1'
}
"""

#使用携带cookie的session进行get请求
detail_page_text = session.get(url=detail_url,headers=headers).text
with open('./chaojiying.html','w',encoding='utf-8') as fp:
    fp.write(detail_page_text)
print('over')







