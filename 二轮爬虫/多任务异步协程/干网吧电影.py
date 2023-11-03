"""
1.一般情况下，网页的视频资源会在<video>标签中
2，现在几乎没有一个网站会将视频地址直接给出在video标签中：
    1.视频缓存过大，给网页带来负担
    2.用户体验差，占网速，占内存
3。基于以上情况，网页会对视频进行切片，每一片都会有独立的url地址
如abc.ts  efg.ts  123.ts
,如果不按正确的顺序进行保存，视频会出现顺序问题
必须把ts文件的正确顺序进行保存  -》M3U文件 -》utf-8 -》M3U8文件


4.正确的视频加载流程：
    1.先请求到M3U8文件
    2.加载ts文件
    3.正常播放视频资源
    这样会使得服务器压力减小，用户体验好


在M3U8文件中，不带#号的都是ts文件，带#号的都有特殊含义
"""
#针对云播TV电影网的分析
import re

"""
1.拿到视频页的页面源代码
2.从视频页的源代码中找到对应的script，提取到script中的url
3.格式化url得到第一层M3U8文件
4.下载第一层M3U8文件，从中解析出第二层的地址
5.下载第二层的M3U8。从第二层文件中解析出每一个TS文件的路径，启动协程
6.对ts文件进行解密操作，先拿key
7.对ts文件进行合并，还原回mp4文件

"""

import requests
from lxml import etree
import json
from urllib.parse import urljoin
import asyncio
import aiohttp
import aiofiles
import os
from Crypto.Cipher import AES


#获取页面源码
def get_page_source(url):
    resp = requests.get(url)
    return resp
    # print(resp.text)

#获取第一层m3u8文件
def get_script_url(url):
    page_source = get_page_source(url).text
    tree = etree.HTML(page_source)
    dic_str = tree.xpath('//*[@id="bofang_box"]/script[1]/text()')[0].strip("var player_aaaa=")  # 提取script中的所有内容
    dic = json.loads(dic_str) #将字符串转为字典格式拿信息
    #print(dic)
    m3u8_1_url = dic['url']
    #print(m3u8_1_url)
    return m3u8_1_url
    #print(page_source)

#下载第二层m3u8文件
def download_m3u8_url(url):
    #通过第一个m3u8文件请求得到第二层m3u8文件并下载保存
    print('开始下载第二层m3u8文件')
    resp = get_page_source(url)
    m3u8_2_url = urljoin(url, resp.text.split()[-1])
    #print(m3u8_2_url)
    #print(resp.text.split()[-1])
    resp2 = get_page_source(m3u8_2_url)
    with open('./他是谁第一集m3u8.txt',mode='wb') as f:
        f.write(resp2.content)
    resp.close()
    print('下载完成')

#如果视频存在加密的话，获取秘钥，

# def get_key():
#     obj = re.compile(r'URL="(?P<key_url>.*?)"')
#     with open('./他是谁第一集m3u8.txt',mode='r',encoding='utf-8') as f:
#         result = obj.search(f.read())
#         key_url = result.group('key_url')
#         #然后发送请求获取key的数值

#针对加密ts文件的解密
#一个一个解密ts文件

# async def des_one():
#     #针对对称加密（AES=128）的解密
#     aes = AES.new(key=key,IV=b'0000000000000000',mode=AES.MODE_CBC) #IV默认16个0
#     # 先读取加密的ts文件
#     async with aiofiles.open(f'./电影源_加密/{file}',mode='rb') as f1,\
#             aiofiles.open(f'./电影源_解密/{file}',mode='wb') as f2:   #写入解密后的ts文件
#         content = await f1.read()
#
#         bs = aes.decrypt(content)#解密，加密为aes.encrypt()
#         await f2.write(bs)
#
#
#     print('文件解密完成')


#开启协程解密所有文件

# async def des_all_ts_file(key):
#         tasks = []
#         with open('他是谁第一集m3u8.txt',mode='r',encoding='utf-8') as f:
#             for line in f:
#                 if line.startswith('#'):  #去除特殊字符串
#                     continue
#                 line = line.strip() #去掉换行符
#                 file_name = line.split('/')[-1]
#                 #准备异步协程
#                 task = asyncio.create_task(line)
#                 tasks.append(task)
#         await asyncio.wait(tasks)



#ts文件单独下载
async def download_one(url): #此处的url为ts的下载路径
    for i in range(10):
        try:
            filename = url.split('/')[-1].strip('\n')
            async with aiohttp.ClientSession() as session:
                async with session.get(url,timeout=30) as resp:
                    content = await resp.content.read() #下载二进制文件
                    async with aiofiles.open('./电影源_加密/'+filename,mode='wb') as f:
                        await f.write(content)
            print('下载成功', url)
            break
        except:
            print('下载出错，重新发送', url)
            await asyncio.sleep((i+1) * 5) #适当的进行睡眠达到提高成功率的目的

#通过第二层m3u8文件开始异步下载所有ts文件
async def download_all_ts():
        tasks = []
        with open('他是谁第一集m3u8.txt',mode='r',encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                task = asyncio.create_task(download_one(line))
                tasks.append(task)
        await asyncio.wait(tasks)


#合并所有ts文件
def merge_ts():
    name_list = []
    with open("他是谁第一集m3u8.txt",mode='r',encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            file_name = line.split('/')[-1].strip('\n')
            name_list.append(file_name)  #通过m3u8文件获取视频顺序

    #print(name_list)
    # 1.记录当前目录
    now_dir = os.getcwd()
    #print(now_dir)
    os.chdir('./电影源_加密')
    #对于数量庞大的ts文件，分而治之，每次可以合并100个
    temp = []
    n = 1
    for i in range(len(name_list)):  #在ts文件保存的目录下根据name_list的顺序进行合并，以保证视频的顺序性
        name = name_list[i]
        temp.append(name)
    #print(temp)
        if i !=0 and i % 100 == 0 :
            #合并
            #cat a.ts b.ts c.ts > xxx.mp4
            #windows采用copy /b a.ts + b.ts + c.ts xxx.mp4合并文件
            names = '+'.join(temp)
            #print(names)
            os.system(f"copy /b {names} {n}.ts")  #先零散合并ts文件
            print(names)
            temp = []  #合并100个后还原为待合并列表
            names = ''
            print(f'{n}.ts下载完成')
            n += 1
    #
    #不够整除100的最后剩余的ts进行收尾
    names = ' + '.join(temp)
    #print(names)
    os.system(f"copy /b {names} {n}.ts")
    n += 1
    #
    temp_2 = []
    #对n进行循环，合并所有零散mp4文件
    for i in range(1,n):
        temp_2.append(f'{i}.ts')
    #print(temp_2)
    names = '+'.join(temp_2)
    #print(names)
    os.system(f"copy /b {names} move1.mp4")

    #工作完后一定要切换回原目录
    os.chdir(now_dir)
    print('合并完成')


def main():
    #下载满江红电影
    # print('主页获取中')
    # print('开始分析m3u8文件')
    # url = 'https://www.ahsnxc.com/vodplay/45042-1-1.html'
    # src_url = get_script_url(url)
    # print('第一层解析完成')
    # download_m3u8_url(src_url)
    # asyncio.run(download_all_ts())

    #开始解密
    # print('开始解密')
    # key = get_key()
    # asyncio.run(des_all_ts_file(key))

    #合并ts文件
    merge_ts()


if __name__ == '__main__':
    main()




































































































