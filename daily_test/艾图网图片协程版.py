import asyncio
import time
import aiofiles
import aiohttp
import requests
from lxml import etree
import re


async def download(src_list):
    tasks = []
    for src in src_list:
        task = asyncio.create_task(download_pic(src))
        tasks.append(task)
    await asyncio.wait(tasks)


async def download_pic(src):
        pic_name = src.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(src) as resp:
                cont = await resp.content.read()
                async with aiofiles.open('./aitu_pic/' + pic_name, mode='wb') as f:
                    await f.write(cont)
                    print(f'{pic_name}下载完成')


def get_pic_url(url):
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        tree = etree.HTML(resp.text)
        pic_url_string = tree.xpath('//html/body/script[2]/text()')[0]
        obj = re.compile(r'var imagesarr=\"(.*?)\";')
        data = obj.findall(pic_url_string)[0]
        data = str(data).replace('&quot;', '')
        data_list = data.split('}')
        pic_url_list = []
        for li in data_list:
            http = re.findall(r'picture:(.*?)/nu', li)
            if not http:
                continue
            else:
                http_str = http[0]
            http = http_str.replace('\\', '')
            pic_url_list.append(http)
        return pic_url_list


def main():
    for i in range(1, 25):
        url = f"https://www.iituku.com/lvyou/index_{i}.html?sort=0"
        pic_url_list = get_pic_url(url)
        asyncio.run(download(pic_url_list))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('耗时为：', end_time-start_time)





























