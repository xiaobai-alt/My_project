# import asyncio
# import time
#
# async def request(url):
#     print('正在下载',url)
#     await asyncio.sleep(2)
#     print('下载完毕',url)
#
# start = time.time()
# urls = [
#     'www.baidu.com',
#     'www.sougou.com',
#     'www.csdn.com'
# ]
# starks = []
# for url in urls:
#     c = request(url)
#     task = asyncio.ensure_future(c)
#     starks.append(task)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(starks))
# print(time.time()-start)


import requests
import asyncio
import time
import aiohttp #使用该模块中的ClientSession

urls = [
    'http://127.0.0.1:5000/chen','http://127.0.0.1:5000/jay','http://127.0.0.1:5000/Tom'
]
start = time.time()
async def request(url):
    print('请求开始',url)
    #response = requests.get(url=url) #request是基于同步的，必须要使用基于异步的网络请求模块
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as response:
                page_text = await response.text()  #在获取响应数据前一定要使用await进行手动挂起
                #text()返回字符串类型的响应数据
                #read()返回二进制类型的响应数据
                #json()返回的json对象
                print('下载完毕',page_text)

tasks = []

for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print('总耗时：',time.time()-start)






















