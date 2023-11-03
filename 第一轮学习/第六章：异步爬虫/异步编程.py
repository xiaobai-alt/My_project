#
# import asyncio
# async def func():
#     print('1')
#     await asyncio.sleep(2)
#     print(2)
#     return '返回值'
#
#
# async def main():
#     print('main开始')
#
#     task_list = {
#         asyncio.create_task(func(),name='a1'), #自定义name，方便结果分析
#         asyncio.create_task(func(),name='a2')
#     }
#
#     done,pending = await asyncio.wait(task_list,timeout=None)  #wait函数针对Task列表
#     print('main结束')
#     print(done)
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(result)
# asyncio.run(main())

import asyncio

async def request(url):
    print('正在请求的url是',url)
    print('请求成功',url)
    return url

#async修饰的函数，调用之后返回的一个协程对象
c = request('www.baidu.com')

#asyncio.run(c) #用来代替loop，可以直接执行  # #创建一个事件循环对象 # loop = asyncio.get_event_loop() # #将协程对象注册到loop中 # loop.run_until_complete(c)

#task的使用
#创建task任务对象
# loop = asyncio.get_event_loop()
# task =  loop.create_task(c)
# print(task)
# loop.run_until_complete(task)
# print(task)

#future的使用
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(c)
# print(task)
# loop.run_until_complete(task)
# print(task)

#绑定回调
def callback_func(task):
    #result返回的就是任务对象总封装的协程对象对应函数的返回值
    print(task.result())
loop = asyncio.get_event_loop()
task = loop.create_task(c,name='test1')
#将回调函数绑定到任务对象中
task.add_done_callback(callback_func)
loop.run_until_complete(task)





















































