# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline  # 导入自有图片管道，定义类继承
import pymysql
from picdownload.settings import MYSQL


class PicdownloadPipeline:
    def process_item(self, item, spider):
        return item


class MeinvMySqlPipeline:

    # 如同其翻译一样，内部函数的执行方法分别在开始与结束时使用
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
            sql = 'insert into meinv (name ,img_src, img_path) values (%s,%s,%s)'

            cursor.execute(sql, (item['name'], item['img_src'], item['img_path']))
            self.conn.commit()
        except:
            self.conn.rollback()
        return item


# 想要使用ImagesPipeline。必须单独设置setting的一个配置，用来保存文件的文件夹
class MeinvPipeline(ImagesPipeline):  # 利用scrapy自有的图片管道进行下载操作，继承其方法
    def get_media_requests(self, item, info):  # 负责下载
        yield scrapy.Request(item['img_src'])  # 这里直接将数据返回给ImagesPipeline

    def file_path(self, request, response=None, info=None, *, item=None):  # 准备文件路径
        # 由于此处函数的item并没有数据，无法获取文件名，所以我们直接通过request获取url再次剪切处文件名
        file_name = request.url.split('/')[-1]
        return f'./img/{file_name}'

    def item_completed(self, results, item, info):  # 返回文件的详细信息
        ok, info = results[0]
        item['img_path'] = info['path']
        return item
