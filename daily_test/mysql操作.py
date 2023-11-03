
import pymysql
from pymysql.cursors import DictCursor  # 导入字典形式的游标

def change(sql, isinsert=False, issele=False):
    try:
        # 第一步创建连接
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='sys'
        )
        # 第二步，创建游标，利用游标来执行sql语句
        cursor = conn.cursor(cursor=DictCursor)
        # 执行sql语句
        count = cursor.execute(sql)
        # 由于pymsql在执行时默认开启事务，事务可以保证在程序出错时将已经编辑的信息撤回，能够保证数据的完整性
        # 关于事务有两个操作：rollback 有问题回滚程序， commit：无问题时提交事务
        # 手动提交事务
        conn.commit()
        if isinsert:  # 判断是否为新增数据
            new_id = cursor.lastrowid  # 获取新增数据的id
            return new_id
        elif issele:
            info = cursor.fetchall()
            return info
        else:
            return count

    except Exception as e:
        print(e)
        conn.rollback()  # 报错回滚数据
    finally:
        if conn:
            conn.close()  # 程序结束后要关闭与数据库的连接


def add(sql,):
    return change(sql, isinsert=True)


def update(sql):
    return change(sql)


def delete(sql):
    return change(sql)


def select(sql):
    # select 查询的信息被放在cursor中
    return change(sql,issele=True)


if __name__ == '__main__':
    # sql = 'insert into stu(sname, sage, sgender, sclass) values ("二傻子", 28, 1, "一年三班")'
    # result = add(sql)
    # print(result)

    # sql = 'update stu set sname="娃哈哈" where sid = 13'
    # result = update(sql)
    # print(result)

    sql = 'select * from stu'
    result = select(sql)
    print(result)





















