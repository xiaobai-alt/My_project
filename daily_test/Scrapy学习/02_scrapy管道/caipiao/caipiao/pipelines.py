# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pymongo
from caipiao.settings import MYSQL
from caipiao.settings import MONGODB

"""
    目前存储数据的基本方案：
        1.数据存储在csv文件中
        2.数据存储在mysql数据库中
        3.数据存储在MongoDB数据库中
        4.以文件的形式存储
"""


# csv存储
class CaipiaoPipeline:

    # 如同其翻译一样，内部函数的执行方法分别在开始与结束时使用
    def open_spider(self, spider):
        self.f = open('./双色球.csv', mode='a', encoding='utf-8')

    def close_spider(self, spider):
        if self.f:
            self.f.close()

    def process_item(self, item, spider):
        # 如果io操作放在此处会导致每执行一次就会进行一次io操作。大大增加了繁琐度与不安全性
        # 所以期望的步骤为在爬虫开启的时候打开需要存储的文件，执行过程中不断往里存入数据，执行完毕时关掉此文件
        # scrapy很好的提供了open_spider,close_spider两个函数，只需要使用者定义这两个方法，scrapy就会自动执行他
        # with open('./双色球.csv', mode='a', encoding='utf-8') as f:
        #     f.write(f'{item["qihao"]},{"_".join(item["red_boll"])},{item["blue_boll"]}\n')
        self.f.write(f'{item["qihao"]},{"_".join(item["red_boll"])},{item["blue_boll"]}\n')
        return item


# mysql存储
class CaipiaoMySqlPipeline:

    # 如同其翻译一样，内部函数的执行方法分别在开始与结束时使用
    def open_spider(self, spider):
        # 可以在此处直接定义参数，也可以在settings文件中定义完成后，用字典的方式引用，方便后续更改数据库
        # self.conn = pymysql.connect(
        #     host='localhost',
        #     port=3306,
        #     user='root',
        #     password='123456',
        #     database='sys'
        # )
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = 'insert into caipiao (qihao,red_boll, blue_boll) values (%s,%s,%s)'

            cursor.execute(sql, (item['qihao'], '_'.join(item['red_boll']), item['blue_boll']))
            self.conn.commit()  # sql语句执行后需要commit才会正式存储进数据库，相当于我们修改完文件后需要ctrl+s保存一样
        except:
            self.conn.rollback()  # rollback方法用于sql语句出错时恢复文件为修改前的内容，类似于ctrl+z，撤回操作
        return item


# MongoDB存储
class CaipiaoMongoDBPipeline:

    # 如同其翻译一样，内部函数的执行方法分别在开始与结束时使用
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=MONGODB['host'], port=MONGODB['port'])
        db = self.client['daliytestdb']  # 指定数据库
        self.collection = db['caipiao']  # 指定集合

    def close_spider(self, spider):
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(
            {'qihao': item['qihao'], 'red_boll': item['red_boll'], 'blue_boll': item['blue_boll']})
        return item
