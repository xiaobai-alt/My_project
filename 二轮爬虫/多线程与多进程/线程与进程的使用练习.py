"""
关于对https://www.tu963.cc/y/2/index.html网址进行图片爬取的过程分析
    进程1.从主页面中获取详情页的url，跳转到详情页获取图片的下载地址
    进程2.使用进程一获取到得下载地址进行图片下载    两个进程之前数据传输必须经过第三方传输（通过队列传输）  队列：通过网络传输
    队列：可以进行进程之间的通信
    此处的队列必须使用multiprocessing中的Queue
"""
from multiprocessing import Process,Queue
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree


def get_img_src(q):
    url = 'https://www.tu963.cc/y/2/index.html'
    response = requests.get(url)
    response.encoding = 'gbk'
    #print(response.text)
    tree = etree.HTML(response.text)
    img_url_list = tree.xpath("//div[@class='listMeinuT']/ul/li")
    img_src_dict = {}
    for li in img_url_list:
        img_name = li.xpath("./a[@class='tit']/text()")[0]
        img_src = li.xpath("./a[@class='tit']/@href")[0]
        img_src_dict[img_name] = img_src
    #print(img_src_dict)
    for value in img_src_dict.values():
        download_index_url = value
        download_index_response = requests.get(download_index_url)
        download_index_response.encoding='gbk'

        down_tree = etree.HTML(download_index_response.text)
        img_src_list = down_tree.xpath("//div[@class='content']/img")
        #print(img_src_list)
        #down_img_url_list = []
        for li in img_src_list:
            down_img_src = li.xpath('./@src')[0]
            #print(down_img_src)
            #down_img_url_list.append(down_img_src)
            q.put(down_img_src)  #像队列中装载url
            print(f"{down_img_src},被装进对列")
            #print(down_img_src)

def download(url):
    #pass
    print('开始下载')
    name = url.split('/')[-1]
    #print(name)
    resp = requests.get(url).content
    #print(resp)
    with open('./img/'+name,mode='wb') as f:
        f.write(resp)
    print('下载完毕',url)


def download_img(q):
    #pass
    with ThreadPoolExecutor(10) as t:  # 利用线程池缓解流量
        while 1:  # 利用死循环获取src
            src = q.get()  # 从队列中获取数据，没有数据时就会阻塞
            t.submit(download, src)


if __name__ == '__main__':
    """
    url:网址地址
    p1:用于获取图片详情页网址的进程
    p2:用于通过获取到详情页的图片的下载地址进行图片下载的进程
    
    """
    q = Queue()
    p1 = Process(target=get_img_src, args=(q,)) #用传参
    p2 = Process(target=download_img, args=(q,))
    p1.start()
    p2.start()














































