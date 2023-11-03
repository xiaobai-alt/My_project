from concurrent.futures import ThreadPoolExecutor
import time
# #常用写法
# def func(name):
#     for i in range(10):
#         print(name,i)
#
# if __name__ == '__main__':
#     with ThreadPoolExecutor(10) as t:
#         for i in range(100):
#             t.submit(func,f'test{i}')


# def func(name,t):
#     time.sleep(t)
#     print('我是',name)
#     return name
#
# def fn(res):
#     print(res.result())
#
# if __name__ == '__main__':
#     with ThreadPoolExecutor(3) as t:
#         # t.submit(func,'周杰伦',3).add_done_callback(fn) # 返回即执行  返回值的返回顺序不确定
#         # t.submit(func, '周润发',2).add_done_callback(fn)
#         # t.submit(func, '王力宏',1).add_done_callback(fn)
#         result = t.map(func,['周杰伦','周润发','王力宏'],[2,3,1]) # 返回的是生成器,且返回的是任务设定的顺序
#         for i in result:
#             print(i)











































