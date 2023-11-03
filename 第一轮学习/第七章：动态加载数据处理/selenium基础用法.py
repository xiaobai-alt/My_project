from selenium import webdriver
from lxml import etree
import time

#实例化一个浏览器对象（传入浏览器的驱动程序）
bp = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')

#让浏览器发起一个指定url对应请求
bp.get('https://www.nmpa.gov.cn/hzhp/hzhpcjgg/hzhpcjgggjj/index.html')

#page_source获取浏览器当前页面的页面源码数据
page_text = bp.page_source

tree = etree.HTML(page_text)
li_list = tree.xpath('//div[@class="list"]/ul')
print(li_list)
for li in li_list:
    name = li.xpath('./a/text()')[0]
    print(name)

time.sleep(5)
bp.quit()







































