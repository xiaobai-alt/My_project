import scrapy


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/typerank?type_name=%E5%96%9C%E5%89%A7&type=24&interval_id=100:90&action="]

    def parse(self, response):
        print(response.text)
