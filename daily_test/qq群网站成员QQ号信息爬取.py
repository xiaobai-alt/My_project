import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from lxml import etree

opt = Options()
opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器

url = 'https://qun.qq.com/#/login'
web = Chrome(options=opt)
web.get(url)
WebDriverWait(web, 1000, 1).until(EC.url_to_be('https://qun.qq.com/#/member-manage/base-manage'))
time.sleep(100)

while 1:
    tree = etree.HTML(web.page_source)

    info_dict = {}
    for i in range(0, 63):
        tree1 = etree.HTML(web.page_source)
        info_list = tree1.xpath('//*[@class="t-table__body"]/tr')
        print(info_list)
        for li in info_list:
            name = li.xpath('./td[1]/div/div/p[1]/text()')[0]
            qq = li.xpath('./td[1]/div/div/p[2]/text()')[0]
            info_dict[name] = qq
            print(name, qq)
        web.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/main/main/div/div/div[2]/div/div/div[2]/div/div/div[3]').click()
        time.sleep(3)

    print(info_dict)
    with open('./qq.txt', mode='w', encoding='utf-8') as f:
        for key in info_dict.keys():
            f.write(key+info_dict[key] + '\n')

    time.sleep(100)

