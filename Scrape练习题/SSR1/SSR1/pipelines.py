# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from SSR1.settings import MYSQL
from twisted.enterprise import adbapi  # 数据量过大时使用异步存储


class Ssr1Pipeline:
    def process_item(self, item, spider):
        return item


class SsrMysqlPipeline:
    def open_spider(self, spider):
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
            sql = 'insert into ssr1 (movie_name, movie_type, movie_area, movie_time, movie_score, movie_detail) values (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (item['movie_name'], item['movie_type'], item['movie_area'], item['movie_time'],
                                 item['movie_score'], item['movie_detail']))
            self.conn.commit()
            cursor.close()
        except:
            self.conn.rollback()
        return item


class SsrAdbMysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 固定函数名格式，会被scrapy调用，直接可以使用settings的值
        """
        数据库建立连接
        :param settings:配置参数
        :return:实例化参数
        """
        adbparams = dict(
            host=MYSQL['host'],
            db=MYSQL['database'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )

        # 连接数据池ConnectionPool
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        return cls(dbpool)  # 返回实例化参数

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和数据
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        insert_sql = "insert into ssr1 (movie_name, movie_type, movie_area, movie_time, movie_score, movie_detail) values (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_sql,
                       (item['movie_name'], item['movie_type'], item['movie_area'], item['movie_time'],
                        item['movie_score'], item['movie_detail']))

    def handle_error(self, failure):
        if failure:
            print(failure)
