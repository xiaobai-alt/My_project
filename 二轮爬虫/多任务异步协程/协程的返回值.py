import asyncio
import time
async def func1():
    print('协程函数1')
    await asyncio.sleep(1)
    print('1执行结束')
    return "func1的返回值"

async def func2():
    print('协程函数2')
    await asyncio.sleep(2)
    print('2执行结束')
    return "func2的返回值"

async def func3():
    print('协程函数3')
    await asyncio.sleep(3)
    print('3执行结束')
    return "func3的返回值"

async def func4():
    print('协程函数4')
    await asyncio.sleep(4)
    print('4执行结束')
    return "func4的返回值"

async def main():
    f1 = func1()
    f2 = func2()
    f3 = func3()
    f4 = func4()
    tasks = [
        asyncio.create_task(f2),
        asyncio.create_task(f3),
        asyncio.create_task(f1),
        asyncio.create_task(f4),
    ]
    # #结果   运行
    # done, pending = await asyncio.wait(tasks)  #asyncio.wait返回的结果是无序的
    # for t in done:
    #     print(t.result())

    result = await asyncio.gather(*tasks,return_exceptions=False)  #  *tasks是将未知参数进行动态传参
    #return_exceptions= False 时，如果有错误信息，所有任务直接停止
    #return_exceptions= True 时，如果有错误信息，返回错误信息，其他任务正常执行
    print(result) #gather结果值按照输入的顺序输出


if __name__ == '__main__':
    start = time.time()

    #将任务放在一起执行

    asyncio.run(main())  #asyncio.wait(tasks)语句意思为等待任务全部完成
    print(time.time() - start)




















