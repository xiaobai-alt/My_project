# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ssr1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    movie_type = scrapy.Field()
    movie_area = scrapy.Field()
    movie_time = scrapy.Field()
    movie_score = scrapy.Field()
    movie_detail = scrapy.Field()
