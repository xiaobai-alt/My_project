import time
import requests
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def get_pic_url():
    url = 'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&keyword=%E6%B7%98%E5%AE%9D%E8%B4%AD%E4%B9%B0%E7%BD%91%E5%BA%97&clk1=3cba19756da969d45754c067b1da5ad5&upsId=3cba19756da969d45754c067b1da5ad5'
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
    opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
    # opt.add_argument("--disable-blink-features=AutomationControlled") # 告诉浏览器去掉了webdriver痕迹

    web = Chrome(options=opt)
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
    })
    web.get(url)
    time.sleep(20)

    tree = etree.HTML(web.page_source)
    goods = tree.xpath("//ul[@class='pc-search-items-list']/li")
    goods_list = []
    for li in goods:
        # print(li.xpath('./a/img/@src'))
        if li.xpath('./a/img/@src'):
            goods_list.append(li.xpath('./a/img/@src')[0])
        elif li.xpath('./a/img/@data-src'):
            goods_list.append(li.xpath('./a/img/@data-src')[0])
    # pic_url_list = []
    for src in goods_list:
        name = (src.split('/')[-1]).rstrip('_.webp')
        print(f'{src}已加载队列')
        resp = requests.get(src).content
        with open('./daily_test/img/' + name, mode='wb') as f:
            f.write(resp)
        print(f'{name}下载完成')


if __name__ == '__main__':
    start_time = time.time()

    get_pic_url()

    end_time = time.time()
    print(end_time - start_time)
