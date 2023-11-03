import scrapy
import json
from SPA1.items import Spa1Item


class SpaSpider(scrapy.Spider):
    name = "SPA"
    allowed_domains = ["spa1.scrape.center"]


    start_urls = [f"https://spa1.scrape.center/api/movie/?limit=10&offset=0"]

    def parse(self, response):
        json_data = json.loads(response.text)
        dict_list = json_data['results']
        item = Spa1Item()
        for dic in dict_list:
            item['name'] = dic['name']
            print(dic['name'])
            str1 = ''
            for i in dic['categories']:
                str1 += i
            print(str1)
            item['categories'] = str1
            item['published_at'] = dic['published_at']
            print(dic['published_at'])
            yield item






