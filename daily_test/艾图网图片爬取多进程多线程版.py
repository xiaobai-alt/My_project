import time
import requests
from lxml import etree
import re
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor


def get_pic_url(q):
    for i in range(1, 25):
        url = f"https://www.iituku.com/lvyou/index_{i}.html?sort=0"
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        tree = etree.HTML(resp.text)
        pic_url_string = tree.xpath('//html/body/script[2]/text()')[0]
        obj = re.compile(r'var imagesarr=\"(.*?)\";')
        data = obj.findall(pic_url_string)[0]
        data = str(data).replace('&quot;', '')
        data_list = data.split('}')
        # pic_url_list = []
        for li in data_list:
            http = re.findall(r'picture:(.*?)/nu', li)
            if not http:
                continue
            else:
                http_str = http[0]
            http = http_str.replace('\\', '')
            # pic_url_list.append(http)
            q.put(http)
            print(f'{http}已加载队列')


def download(src):
        resp = requests.get(src)
        pic_name = src.split('/')[-1]
        with open('./aitu_pic/'+pic_name, mode='wb') as f:
            f.write(resp.content)
        print(f'{pic_name}下载完成')


def download_pic(q):
    with ThreadPoolExecutor(10) as t:
        while True:
            if not q.empty():
                src = q.get()
                t.submit(download, src)
            else:
                break


if __name__ == '__main__':

    q = Queue()
    p1 = Process(target=get_pic_url, args=(q,)) # 进程一用来获取图片链接
    p2 = Process(target=download_pic, args=(q,))  # 进程二用来下载图片
    start_time = time.time()
    p1.start()
    time.sleep(4)
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()
    print(end_time-start_time)





























