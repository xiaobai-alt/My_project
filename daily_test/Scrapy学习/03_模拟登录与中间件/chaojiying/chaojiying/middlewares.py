# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import pickle
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
import requests
import json


class ChaojiyingSpiderMiddleware:
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


class ChaojiyingDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if not request.cookies:
            request.cookies = self.cookie
        return None

    def spider_opened(self, spider):
        opt = Options()
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        opt.add_experimental_option('detach', True)
        web = Chrome(options=opt)
        script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
        web.execute_script(script)
        web.get('http://www.chaojiying.com/user/login/')
        web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys('Mrchen123')
        web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys('chenhao#include0')
        img = web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/div/img')
        verify_code = self.base64_api('chen0525', 'chen123', img.screenshot_as_base64, 3)
        web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(verify_code)
        web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
        time.sleep(2)
        self.cookie = {item['name']:item['value'] for item in web.get_cookies()}

    def base64_api(self, uname, pwd, img, typeid):
        data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
            return result["message"]
        return ""
