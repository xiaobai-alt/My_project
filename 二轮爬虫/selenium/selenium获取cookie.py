from selenium.webdriver import Chrome

web = Chrome()

web.get('http://www.baidu.com')

cookies = web.get_cookies()
print(cookies)

cookie_dic = {}

for dic in cookies:
    key = dic['name']
    value = dic['value']
    cookie_dic[key] = value
print(cookie_dic)

cookie_dic = {dic['name']:dic['value'] for dic in cookies}  #字典生成式 》列表生成式
#当你已经有一个字典形式的cookie，可以直接把整个字典作为参数传递给requests
import requests
headers = {

}

requests.get(url,headers=headers,cookies=cookie_dic)  #直接把cookie当成参数传递（必须是字典）
































































