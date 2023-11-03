# import time
# #使用单线程串行方式执行
#
# def get_page(str):
#     print('正在下载：',str)
#     time.sleep(2)
#     print('下载成功：',str)
#
# name_list = ['xiaozi','aa','bb','cc']
#
# start_time = time.time()
#
# for i in range(len(name_list)):
#     get_page(name_list[i])
#
# end_time = time.time()
# print(f'{end_time-start_time} second')

# import time
# #导入线程池模块对应的类
# from multiprocessing.dummy import Pool
# #使用线程池方式执行
#
# start_time = time.time()
# def get_page(str):
#     print('正在下载：',str)
#     time.sleep(2)
#     print('下载成功：',str)
#
# name_list = ['xiaozi','aa','bb','cc']
#
# #实例化一个线程池对象
# pool =Pool(4)
# #将列表中每一个列表元素传递给get_page进行处理
# pool.map(get_page,name_list)
# end_time = time.time()
# print(f'{end_time-start_time} second')


#需求：爬取梨视频的视频数据
import requests
from lxml import etree
import random
import re
from multiprocessing import Pool
#线程池使用原则：处理的是阻塞且耗时的操作
session = requests.session()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    }
renwu_url = 'https://www.pearvideo.com/category_1'
page_text = session.get(url=renwu_url,headers=headers).text
tree = etree.HTML(page_text)

vivo_url_list =tree.xpath('//*[@id="listvideoListUl"]/li')

urls = []
for li in vivo_url_list:
    """
    vivo_url:视频详情页面
    name：视频名称
    ajex_url：保存视频动态变化的真实网址的网址
    contid：不同视频有不同的身份id
    mrd：与contid一样同为视频真实地址携带的参数，用随机数生成
    vivo_content_url：保存在ajex_url网址json中的真实视频链接
    url：经过最终处理后得到的视频下载链接
    dic：用来保存文件名与链接的字典
    urls：保存所有dic的列表
    """
    vivo_url =  'https://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
    name = li.xpath('./div/a/div[2]/text()')[0] +'.mp4'
    ajex_url = 'https://www.pearvideo.com/videoStatus.jsp?'

    digitals = re.compile(r'\d+',re.I)
    id = li.xpath('./div/a/@href')[0]
    contid = re.findall(digitals,id)[0]
    mrd = random.random()
    headers1={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Referer' :  vivo_url
    }
    param = {
        'contId' : contid,
        'mrd':mrd
    }
    josn_text = session.get(url=ajex_url,params=param,headers=headers1).json()

    vivo_content_url = ((josn_text.get('videoInfo')).get('videos')).get('srcUrl')
    ex = re.compile(r"\d{13}")
    m = ex.findall(vivo_content_url)[0]
    cont = 'cont-' + contid
    url = str(vivo_content_url).replace(m,cont)
    dic = {
        'name':name,
        'url':url
    }
    urls.append(dic)
    # vivo_content = session.get(url=url,headers=headers).content
    # with open(name,'wb') as fp:
    #     fp.write(vivo_content)
    #     print('over')
#使用线程池请求下载
def get_video_data(dic):
    url = dic['url']
    filename = dic['name']
    print(filename,'.....正在下载')
    data = session.get(url=url,headers=headers).content
    with open(filename,'wb') as fp:
        fp.write(data)
        print(filename,'下载成功')
if __name__ == '__main__':
    pool = Pool(4)
    pool.map(get_video_data,urls)
    pool.close()
    pool.join()










































