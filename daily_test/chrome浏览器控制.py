import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lxml import etree

if __name__ == '__main__':
    os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="F:\selenium"')

    # 此乃精髓
    input('输入空格继续程序...')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    browser = webdriver.Chrome(options=options)

    # print(browser.title)
    # print()
    tree = etree.HTML(browser.page_source)
    title = tree.xpath('//*[@id="exploreFeeds"]/section[1]/div/div/a/span/text()')[0]
    # //*[@id="exploreFeeds"]/section[1]/div/div/a/span
    user_name = tree.xpath('//*[@id="exploreFeeds"]/section[1]/div/div/div/a/span/text()')[0]
    print('title:', title)
    print('user_name', user_name)

    # 这里是你的其它逻辑
    """获取粉丝数量
       获取所有新增文章
       获取所有文章的观看数量
    """

