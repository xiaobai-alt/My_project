import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="F:\selenium"')

    # 在此之前的任何操作不会影响到后续逻辑，建议手动完成登录操作
    input('输入空格继续程序...')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    browser = webdriver.Chrome(options=options)

    print(browser.title)
    print()
    # tree = etree.HTML(browser.page_source)
    # title = tree.xpath('//*[@id="exploreFeeds"]/section[1]/div/div/a/span/text()')[0]
    # # //*[@id="exploreFeeds"]/section[1]/div/div/a/span
    # user_name = tree.xpath('//*[@id="exploreFeeds"]/section[1]/div/div/div/a/span/text()')[0]
    # print('title:', title)
    # print('user_name', user_name)

    # 这里是你的其它逻辑
    """获取粉丝数量
       获取所有新增文章
       获取所有文章的观看数量
    """
