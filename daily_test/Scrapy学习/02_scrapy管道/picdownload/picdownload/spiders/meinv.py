import scrapy
from picdownload.items import PicdownloadItem
from urllib.parse import urljoin


class MeinvSpider(scrapy.Spider):
    name = "meinv"
    allowed_domains = ["tu9633.com"]
    start_urls = ["https://www.tu9633.com/y/2/index.html"]

    def parse(self, resp):
        li_list = resp.xpath('//div[@class="listMeinuT"]/ul/li')
        for li in li_list:
            href = li.xpath('./a[1]/@href').extract_first()
            # 如果是自我编写的爬虫程序，那么就需要再次进行请求获取图片链接。但是scrapy中我们只需将获取的url封装起来，引擎会自己识别
            # 封装的内容是数据还是新的请求。数据就存储，新的请求就发送给调度器
            yield scrapy.Request(
                url=href,
                method='get',
                callback=self.parse_next
                # 此处需要自己定义收集返回数据的函数,即回调函数，用于处理回去反馈后处理响应内容
                # 对于进入链接页发现链接页为多页面时，再次采用相同的方法定义函数
            )
        # 注意，上面我们对主页面的第一页内容进行了参数获取与请求，那么可以直接在这里考虑主界面下一页
        # 如果在此处可以开启下一页的话，那么就还是在当前的这个parse进行操作，无需像普通爬虫那样利用协程暴力攻击
        # 判断页面url列表中a字段是否包含“下一页”来确定下一页跳转url
        # next_url = resp.xpath('//div[@class="TagPage"]/ul/li/a[contains(text(),"下一页")]/@href').extract_first()
        # if next_url:
        #     yield scrapy.Request(
        #         url=resp.urljoin(next_url),
        #         callback=self.parse  # 交给parse执行请求操作
        #     )

    def parse_next(self, resp):
        print(resp.url, '请求成功')
        src_list = resp.xpath('//div[@class="content"]/img/@src').extract()
        item = PicdownloadItem()
        for src in src_list:
            name = src.split('/')[-1]
            item['name'] = name
            item['img_src'] = src
            yield item
        next_src = resp.xpath('//div[@class="page-tag oh"]/ul/li/a[contains(text(), "下一页")]/@href').extract_first()
        if next_src:
            yield scrapy.Request(
                url=resp.urljoin(next_src),
                callback=self.parse_next
            )
