# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CaipiaoItem(scrapy.Item):
    # define the fields for your item here like:
    qihao = scrapy.Field()  # 相当于字典中的key
    red_boll = scrapy.Field()
    blue_boll = scrapy.Field()

