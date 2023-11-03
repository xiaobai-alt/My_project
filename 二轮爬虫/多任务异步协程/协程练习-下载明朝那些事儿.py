"""
url:https://www.mingchaonaxieshier.com/
1.获取所有章节src
2.利用协程下载全部章节内容

"""
import asyncio

import requests
import aiohttp
import aiofiles
from lxml import etree
import time

def get_url(url):
    headers = {
        'User - Agent':
    'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/111.0'
    }
    resp = requests.get(url,headers=headers)
    resp.encoding = 'utf-8'
    #print(resp.text)
    src_tree = etree.HTML(resp.text)
    title_list = src_tree.xpath('//div[@class="bg"]/div/center/table/tr[1]/td//a/@href')
    return title_list

def get_title_url(title_list):
    while 1:
        try:
            src_list = []
            headers = {
                'User - Agent':
                    'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/111.0'
            }
            for li in title_list:
                resp = requests.get(li,headers=headers)
                resp.encoding = 'utf-8'
                #print(resp.text)
                tree = etree.HTML(resp.text)
                ul_list = tree.xpath("//div[@class='content']/ul/li/a/@href")
                for src in ul_list:
                    src_list.append(src)
            #print(src_list)
            return src_list
                    #print(ul_list)
        except:
            print('正在重连')
            time.sleep(2)

    #print(title_list)

async def download_one(href):
    async with aiohttp.ClientSession() as session:
        async with session.get(href) as resp:
            page_source = await resp.text()
            #print(page_source)
            tree = etree.HTML(page_source)
            title = tree.xpath("//div[@class='main']/h1/text()")[0]
            content = '\n'.join(tree.xpath("//div[@class='content']/p/text()"))
            #print(title)
            #print(content)
            async with aiofiles.open(f'./明朝那些事儿/{title}.txt',mode='w',encoding='utf-8') as f:
                await f.write(content)
    print('下载完毕',href)

async def dowload(href_list):
    task = []
    for href in href_list:
        t = asyncio.create_task(download_one(href))
        task.append(t)
        #break
    await asyncio.wait(task)


def main():
    #1.拿到页面中的没一个章节的url
    #2.启动协程，开始一节一节下载
    url = 'https://www.mingchaonaxieshier.com/'
    mulu_href_list = get_url(url)
    href_list = get_title_url(mulu_href_list)
    asyncio.run(dowload(href_list))



if __name__ == '__main__':
    main()









































