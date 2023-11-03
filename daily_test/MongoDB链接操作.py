import pymongo


def get_con():
    # 创建链接
    client = pymongo.MongoClient(host='localhost', port=27017)

    # 切换数据库
    db = client['daliytestdb']
    return db


def add_one(collection_name, data):
    db = get_con()
    result = db[collection_name].insert_one(data)
    print(result)
    return result


def add_many(collection_name, data):
    db = get_con()
    result = db[collection_name].insert_many(data)
    print(result)
    return result


def update(collection_name, condition, prepare):
    db = get_con()
    result = db[collection_name].update_one(condition, prepare)
    return result


def delete(collection_name, condition):
    db = get_con()
    result = db[collection_name].delete_many(condition)
    print(result)
    return result


def query(collection_name, condition):
    db = get_con()
    result = db[collection_name].find(condition)
    return list(result)


if __name__ == '__main__':
    # add_one('test2', {'sname': 'tom1', 'sage': 19, 'sgender': 1, 'hobby': ['唱', '跳']})
    # add_many('test2', [{'sname': '张三', 'sage': 19, 'sgender': 1}, {'sname': '李四', 'sage': 29, 'sgender': 0},
    #                    {'sname': '李六', 'sage': 18, 'sgender': 1}])
    # update('test2', {'sname': '李六'}, {'$set': {'sage': 28}})
    # delete('test2', {'sname': 'tom1'})
    result = query('test2', {'sname': {'$regex': '^李'}})
    print(result)
