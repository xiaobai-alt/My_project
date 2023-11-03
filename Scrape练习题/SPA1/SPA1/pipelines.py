# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from SPA1.settings import MYSQL


class Spa1Pipeline:
    def process_item(self, item, spider):
        return item


class Spa1MysqlPipeline:
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
            sql = 'insert into spa1(movie_name, movie_categories, movie_published) values (%s, %s, %s)'
            cursor.execute(sql, (item['name'], item['categories'], item['published_at']))
            self.conn.commit()
            cursor.close()
        except:
            self.conn.rollback()
        return item
