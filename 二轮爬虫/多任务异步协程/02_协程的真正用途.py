import asyncio
import time
import aiohttp
import aiofiles
# async def func1():
#     print('协程函数1')
#     await asyncio.sleep(1)
#     print('1执行结束')
#
# async def func2():
#     print('协程函数2')
#     await asyncio.sleep(2)
#     print('2执行结束')
# async def func3():
#     print('协程函数3')
#     await asyncio.sleep(3)
#     print('3执行结束')
#
# async def func4():
#     print('协程函数4')
#     await asyncio.sleep(4)
#     print('4执行结束')
#
# if __name__ == '__main__':
#     start = time.time()
#     f1 = func1()
#     f2 = func2()
#     f3 = func3()
#     f4 = func4()
#     #将任务放在一起执行
#     tasks = [
#         f1,
#         f2,
#         f3,
#         f4,
#     ]
#     asyncio.run(asyncio.wait(tasks))  #asyncio.wait(tasks)语句意思为等待任务全部完成
#     print(time.time() - start)

async def download(url, t):
    file_name = url.split('/')[-1]
    #相当于request，但request不是异步的
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()  #
            #异步条件下写入文件
            async with aiofiles.open(file_name,mode='wb') as f:
                await f.write(content)



async def main():
    #假设此处为多个下载链接
    urls = [
        'https://www.baidu.com',
        'https://cehsi.com',
        'https://www.sougou.com',
    ]
    tasks = []
    for url in urls:
        #创建任务
        task = asyncio.create_task(download(url,3)) #asyncio.wait(tasks)方法在3.8以上会报警告，需要用此方法解决
        tasks.append(task)
    #统一处理
    await asyncio.wait(tasks)  #在协程中若想等待整体执行完成，需要加上await 函数

if __name__ == '__main__':
    asyncio.run(main())





































