# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 管道默认不开启，需要到settings文件开启
class Game4399Pipeline:
    def process_item(self, item, spider):  # 此处方法名不要改，item：数据  spider：爬虫
        print(item)
        print(spider.name)
        return item  # 必须要return，否则下一个管道收不到数据
