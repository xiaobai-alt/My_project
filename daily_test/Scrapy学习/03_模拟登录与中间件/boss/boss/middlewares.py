# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from boss.request import SeleniumRequest
from selenium.webdriver import Chrome
from scrapy.http.response.html import HtmlResponse


class BossSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BossDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.用于创建爬虫程序的核心
        s = cls()  # 可以看到下列的方法，第一个参数为执行什么方法  ，第二个参数为执行的时间
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed,signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # 所有请求集中此处，进行selenium操作。返回页面源代码组装的response
        # 为了避免不用selenium操作的爬虫经过，需要进行判断
        # isinstance 用来判定xxx是不是xxx类型的
        if isinstance(request, SeleniumRequest):  # 将需要selenium操作的爬虫，内部使用SeleniumRequest请求继承request
            self.web.get(request.url)
            # 由于此处的return返回只有三种，存在限制，所以需要封装响应对象
            page_source = self.web.page_source
            return HtmlResponse(url=request.url, status=200, body=page_source, request=request, encoding='utf-8')
        else:
            return None

    def spider_opened(self, spider):
        self.web = Chrome()

    def spider_closed(self, spider):
        self.web.close()
