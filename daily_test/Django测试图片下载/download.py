import requests
from lxml import etree
from urllib.parse import urljoin
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor


def get_variety_url(list, q):
    for src in list:
        resp = requests.get(src)
        tree1 = etree.HTML(resp.text)
        u_list = tree1.xpath("//div[@id='zoom']/p")
        for u in u_list:
            url_d = u.xpath('./img/@src')
            if not url_d:
                continue
            else:
                url_d = url_d[0]
                q.put(url_d)
                print(url_d, '已放入队列')


def get_index(q, url):
    response = requests.get(url)
    response.encoding = 'gbk'
    tree = etree.HTML(response.text)
    url_list = []
    href_list = tree.xpath("//ul[@class='g-gxlist-imgbox']/li")
    for li in href_list:
        href = li.xpath('./a/@href')[0]
        src = urljoin(url, href)
        url_list.append(src)
    get_variety_url(url_list, q)


def download(url):
    print('等待下载')
    name = str(url).split('/')[-1]
    resp = requests.get(url).content
    with open('./download/' + name, mode='wb') as f:
        f.write(resp)
    print(name, '下载完成')


def download_img(q):
    with ThreadPoolExecutor(30) as t:
        while True:
            src = q.get()
            t.submit(download, src)


if __name__ == '__main__':
    q = Queue()
    url = 'https://www.qqtn.com/tp/fjtp_1.html'
    p1 = Process(target=get_index, args=(q, url))
    p2 = Process(target=download_img, args=(q,))
    p1.start()
    p2.start()
