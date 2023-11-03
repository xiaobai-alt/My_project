# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MidSpiderMiddleware:
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


# 下载器中间件  位于下载器与引擎之间
class MidDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        在引擎将请求的信息交给下载器之前，自动调用该方法
        :param request: 当前请求
        :param spider: 发出该请求的爬虫
        :return:
            注意  ，process_request返回值是有规定的
            1.如果返回None，表示不做拦截，继续向后面的中间件执行，
            2.如果返回的是Request，后续的中间件不在执行，将请求重新交给引擎，引擎重新交给调度器
            3.如果返回的是Response ，后续的中间件不执行，将响应信息交给引擎，引擎将响应丢给spider，进行数据处理

        """
        print('我是process_request')
        return None

    def process_response(self, request, response, spider):
        """
        在下载器返回响应准备交给引擎之前，自动执行
        :param request: 当前请求
        :param response: 响应内容
        :param spider: 发送请求的爬虫
        :return:
            1、request 直接把请求交给引擎，丢给调度器
            2、response 继续想前进行提交返回
        """
        print('我是process_response')
        return response

    def process_exception(self, request, exception, spider):
        # 程序出错时，执行
        pass

    def spider_opened(self, spider):
        # spider.logger.info("Spider opened: %s" % spider.name)
        print('我是spider_opened1')


# 下载器中间件  位于下载器与引擎之间
class MidDownloaderMiddleware2:

    def process_request(self, request, spider):

        print('我是process_request2')
        return None

    def process_response(self, request, response, spider):

        print('我是process_response2')
        return response

