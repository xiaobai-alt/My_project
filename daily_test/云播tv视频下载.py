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
import asyncio
import requests
from lxml import etree
import json
from urllib.parse import urljoin
import aiohttp
import aiofiles
import time


# 下载第二层m3u8文件
def down_sec_m3u8(url):
    resp = requests.get(url).text
    with open('./download_video/全职高手第一集m3u8.txt', mode='w', encoding='utf-8') as f:
        f.write(resp)
    print('下载完成')


# 定义函数获取第一层m3u8文件
def get_first_m3u8(url):
    resp = requests.get(url).text
    tree = etree.HTML(resp)
    dic_str = tree.xpath('//*[@id="bofang_box"]/script[1]/text()')[0].strip("var player_aaaa=")  # 提取script中的所有内容,此时为字符串形式
    dic = json.loads(dic_str)  # 将字符串转为字典形式便于获取url
    first_m3u8_url = dic['url']
    sec_resp = requests.get(first_m3u8_url).text
    sec_url = urljoin(first_m3u8_url, sec_resp.split()[-1])
    return sec_url


async def down_one_ts(url):
    while 1:  # 写死循环不断请求
        try:
            filename = url.split('/')[-1].strip()
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.content.read()
                    async with aiofiles.open('./download_video/video_ts/'+filename, mode='wb') as f:
                        await f.write(data)
            print(url + '下载成功')  # 一个文件下载成功后直接终止循环
            break
        except:
            print('下载出错，正在重新发送请求'+url)
            await asyncio.sleep(2)  # 进行适当睡眠让浏览器反应能增加成功率


async def down_all_ts():
    tasks = []
    with open('./download_video/全职高手第一集m3u8.txt', mode='r', encoding='utf-8') as f:
        for li in f:
            if li.startswith('#'):  # 观察文件发现#开头的都是特殊解释，不是路径，所以去除
                continue
            else:
                task = asyncio.create_task(down_one_ts(li))
                tasks.append(task)
    await asyncio.wait(tasks)


# 定义main函数作为函数运行主体
def main():
    url = 'https://www.ahsnxc.com/vodplay/31584-1-1.html'  # 自己想要下载的视频url
    second_m3u8_url = get_first_m3u8(url)  # 获取第一个m3u8文件,并提取出第二层m3u8文件的地址
    down_sec_m3u8(second_m3u8_url)
    asyncio.run(down_all_ts())


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('下载时间为:', end_time-start_time)
































