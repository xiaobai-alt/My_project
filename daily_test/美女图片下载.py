"""
设计思路，首先获取国产区首页链接，然后获取到每个页面的链接，进入不同页面链接后获取当前页面所有美女写真种类种类链接。
根据获取到的种类链接进入后获取种类的页面链接，并获取当前种类页面所以图片下载链接


"""
import asyncio
import time
import aiofiles
import aiohttp
import requests
from lxml import etree


# async def get_index_url(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             data = await resp.text()
#             tree = etree.HTML(data)
#             beautify = tree.xpath('//div[@class="listMeinuT"]/ul/li')
#             beautify_girl_list = [li.xpath('./a/@href')[0] for li in beautify]
#             print('当前页面种类已获取')
#             return beautify_girl_list

def get_index_url(url):
    requests.adapters.DEFAULT_RETRIES = 5
    resp = requests.get(url).text
    tree = etree.HTML(resp)
    beautify = tree.xpath('//div[@class="listMeinuT"]/ul/li')
    beautify_girl_list = [li.xpath('./a[1]/@href')[0] for li in beautify]
    print('当前页面种类已获取')
    return beautify_girl_list


# async def get_varyety_index_url(list):
#         print('跳转成功，正在获取种类下属页面所有图片链接')
#         for src in list:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(src) as resp:
#                     data = await resp.text()
#                     tree = etree.HTML(data)
#                     last_page_num = ([li.xpath('./a/text()')[0] for li in tree.xpath('//div[@class="page-tag oh"]/ul/li')][-2])
#                     last_page_num = int(last_page_num)
#                     return last_page_num, src


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
        for i in range(1, num+1):
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

# async def get_variety_url(num, src):
#     src_start = src
#     beautify_girl_list = []
#     tasks=[]
#     for i in range(1, num+1):
#         if i == 1:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(src) as resp:
#                     data = await resp.text()
#                     tree = etree.HTML(data)
#                     # for li in tree.xpath('.//div[@class="content"]/img'):
#                     #     url = li.xpath('./@src')[0]
#                     #     print(url,'链接已发送')
#                     #     task = asyncio.create_task(download(url))
#                     #     tasks.append(task)
#                     # await asyncio.wait(tasks)
#                     beautify_girl_list += [li.xpath('./@src')[0] for li in tree.xpath('.//div[@class="content"]/img')]
#                     print(src, '页面链接列表获取成功，开始发送')
#
#         else:
#             src = src_start.replace('.html', f'_{i}.html')
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(src) as resp:
#                     data = await resp.text()
#                     tree = etree.HTML(data)
#                     # for li in tree.xpath('.//div[@class="content"]/img'):
#                     #     url = li.xpath('./@src')[0]
#                     #     print(url,'链接已发送')
#                     #     task = asyncio.create_task(download(url))
#                     #     tasks.append(task)
#                     # await asyncio.wait(tasks)
#                     beautify_girl_list += [li.xpath('./@src')[0] for li in tree.xpath('.//div[@class="content"]/img')]
#                     print(src, '页面链接列表获取成功，开始发送')
#
#     return beautify_girl_list


async def download_pic(src):
    filename = src.split('/')[-1]
    print(filename, '开始下载')
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as resp:
            cont = await resp.content.read()
            async with aiofiles.open('./beautify_china_girl/'+filename, mode='wb') as f:
                await f.write(cont)
                print(filename, '下载完成')


async def download(list):
        print(list)
        tasks = []
        for src in list:
            print(src, '链接已获取，发送下载请求')
            task = asyncio.create_task(download_pic(src))
            tasks.append(task)
        await asyncio.wait(tasks)
        # if pending:
        #     print("取消超时任务")
        #     for p in pending:
        #         p.cancel()

def main():
    """
    分析页面发现不同页面之间跳转的链接变动不大，省去了请求首页再获取不同页面链接的步骤，非常nice
    https: // www.tu9633.com / y / 2 / list_2_1.html 变更处只有list_2_1.html这里，第二页就是2_2.html
    鼠标移动到末页发现链接为https: // www.tu9633.com / y / 2 / list_2_1170.html，说明主页面的分页面最多为1170
    """
    for i in range(1, 2):
        index_url = f'https://www.tu9633.com/y/2/list_2_{i}.html'
        # 第一层方法，用于获取国产区所有美女种类的跳转链接，得到的是一个个塞满了链接的列表
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        variety_index_url_list = get_index_url(index_url)
        #print(variety_index_url_list)
        pic_dict = get_variety_index_url(variety_index_url_list)
        #print(pic_dict)
        beautify_girl_list = get_variety_url(pic_dict)
        #print(beautify_girl_list)
        asyncio.run(download(beautify_girl_list))
        print(f"第{i}页图片已下载完成")


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('总耗时为:', end_time-start_time)










































































