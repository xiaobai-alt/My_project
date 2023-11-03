import asyncio


async def func():  #此时返回的是协程对象
    print('我是函数')


if __name__ == '__main__':  #主函数，程序的入口
    # envent_loop = asyncio.get_event_loop()  #必须借助envet_loop拿到事件循环
    # envent_loop.run_until_complete(func())  #该语句表示执行协程对象，直到该对象内的内容执行完毕为止
    asyncio.run(func())






















