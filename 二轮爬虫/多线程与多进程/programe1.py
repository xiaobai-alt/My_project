# #最基本的线程的创建
# from threading import Thread
# #1创建任务
# def func(name):
#     for i in range(3):
#         print(name,i)
# if __name__ == '__main__':
#     #创建线程
#     t1 = Thread(target=func,args=('test1',))
#     t2 = Thread(target=func, args=('test2',))
#     t3 = Thread(target=func, args=('test3',))
#     t1.start()
#     t2.start()
#     t3.start()

# #面向对象写法
# from threading import Thread
# class MyThread(Thread):
#     def __init__(self,name):
#         super(MyThread, self).__init__()
#         self.name = name
#
#     def run(self) -> None:
#         for i in range(1000):
#             print(self.name,i)
#
# if __name__ == '__main__':
#     t1 = MyThread('test1')
#     t2 = MyThread('test2')
#     t1.start()
#     t2.start()


























