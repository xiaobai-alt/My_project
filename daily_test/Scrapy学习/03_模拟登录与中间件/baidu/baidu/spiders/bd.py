import scrapy


class BdSpider(scrapy.Spider):
    name = "bd"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://baidu.com"]

    def parse(self, response):
        print(response)
