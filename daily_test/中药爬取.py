import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from lxml import etree

url = 'https://www.hxzylt.com/forums/488/'
web = Firefox()
web.get(url)

time.sleep(5)
list = []
for i in range(0, 11):
    tree = etree.HTML(web.page_source)

    title_list = tree.xpath('//*[@class="structItemContainer-group js-threadList"]/div')
    for item in title_list:
        title = item.xpath('./div[2]/div/a[2]/text()')[0]
        list.append(title)
        print(title)
    if i == 0:
        web.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/div[2]/div/div/div[3]/div[1]/nav/div[1]/a').click()
    else:
        web.find_element(By.XPATH,
                         '/html/body/div[1]/div[4]/div/div[3]/div[2]/div/div/div[1]/div/nav/div[1]/a[2]').click()



    time.sleep(3)
with open('./2.txt', mode='w', encoding='utf-8') as f:
    for field in list:
        f.write(field + '\n')

