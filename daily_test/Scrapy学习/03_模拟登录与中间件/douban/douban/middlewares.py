# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from douban.settings import USER_AGENT_LIST, PROXY_IP_LIST  # 从setting文件获取已经设置好的ua列表
from random import choice  # 可以随机从列表抽取一个


class DoubanSpiderMiddleware:
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


class DoubanDownloaderMiddleware:

    def process_request(self, request, spider):
        ua = choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua
        return None  # 此处的return要么删除，要么返回None


# 此处先用免费代理测试一下  缺点速度极慢且成功率极低
class ProxyDownloaderMiddleware:
    def process_request(self, request, spider):
        ip = choice(PROXY_IP_LIST)
        request.meta['proxy'] = "https://" + ip
        return None

# 人民币玩家 根据网上付费代理调用api接口使用
class MoneyProxyDownloaderMiddleware:
    def process_request(self,request,spider):
        pass
