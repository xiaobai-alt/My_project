"""
关于对https://www.tu963.cc/y/2/index.html网址进行图片爬取的过程分析
    进程1.从主页面中获取详情页的url，跳转到详情页获取图片的下载地址
    进程2.使用进程一获取到得下载地址进行图片下载    两个进程之前数据传输必须经过第三方传输（通过队列传输）  队列：通过网络传输
    队列：可以进行进程之间的通信
    此处的队列必须使用multiprocessing中的Queue
"""
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree

def get_variety_index_url(list):
    print('跳转成功，正在获取种类下属页面所有图片链接')
    dict_pic = {}
    for src in list:
        requests.adapters.DEFAULT_RETRIES = 5  # 连接失败重连五次
        resp = requests.get(src).text
        tree = etree.HTML(resp)
        last_page_num = ([li.xpath('./a/text()')[0] for li in tree.xpath('//div[@class="page-tag oh"]/ul/li')][-2])
        last_page_num = int(last_page_num)
        dict_pic[src] = last_page_num
    return dict_pic


def get_variety_url(dic):
    beautify_girl_list = []
    for src in dic.keys():
        src_start = src
        num = dic.get(src)
        for i in range(1, num + 1):
            if i == 1:
                requests.adapters.DEFAULT_RETRIES = 5
                data = requests.get(src).text
                tree = etree.HTML(data)
                beautify_girl_list += [li.xpath('./@src')[0] for li in tree.xpath('.//div[@class="content"]/img')]
                print(src, '页面链接列表获取成功，开始发送')

            else:
                src = src_start.replace('.html', f'_{i}.html')
                requests.adapters.DEFAULT_RETRIES = 5
                data = requests.get(src).text
                tree = etree.HTML(data)
                beautify_girl_list += [li.xpath('./@src')[0] for li in tree.xpath('.//div[@class="content"]/img')]
                print(src, '页面链接列表获取成功，开始发送')
    return beautify_girl_list


def get_img_src(q, url):
    response = requests.get(url)
    response.encoding = 'gbk'
    # print(response.text)
    tree = etree.HTML(response.text)
    beautify = tree.xpath("//div[@class='listMeinuT']/ul/li")
    beautify_girl_list = [li.xpath('./a[1]/@href')[0] for li in beautify]
    print('当前页面种类已获取')
    pic_dict = get_variety_index_url(beautify_girl_list)
    pic_src_list = get_variety_url(pic_dict)
    for src in pic_src_list:
        q.put(src)
        print(src, '被装进队列')


def download(url):
    # pass
    print('开始下载')
    name = url.split('/')[-1]
    # print(name)
    resp = requests.get(url).content
    # print(resp)
    with open('./img/' + name, mode='wb') as f:
        f.write(resp)
    print('下载完毕', url)


def download_img(q):
    # pass
    with ThreadPoolExecutor(30) as t:  # 利用线程池缓解流量
        while 1:  # 利用死循环获取src
            src = q.get()  # 从队列中获取数据，没有数据时就会阻塞
            t.submit(download, src)


def main():
    for i in range(1, 2):
        index_url = f'https://www.tu9633.com/y/2/list_2_{i}.html'
        q = Queue()
        p1 = Process(target=get_img_src, args=(q, index_url))
        p2 = Process(target=download_img, args=(q,))
        p1.start()
        p2.start()


if __name__ == '__main__':
    """
    url:网址地址
    p1:用于获取图片详情页网址的进程
    p2:用于通过获取到详情页的图片的下载地址进行图片下载的进程

    """
    main()
