import scrapy


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["chaojiying.com"]
    start_urls = ["http://www.chaojiying.com/user/"]

    def parse(self, response):
        print(response.text)
