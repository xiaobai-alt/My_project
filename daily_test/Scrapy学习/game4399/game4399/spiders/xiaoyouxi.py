import scrapy


class XiaoyouxiSpider(scrapy.Spider):
    name = "xiaoyouxi"
    allowed_domains = ["4399.com"]
    start_urls = ["http://www.4399.com/flash/"]

    def parse(self, response):
        # 无需导入lxml包，可以直接使用xpath获取数据

        # # 获取界面游戏名称
        # txt = response.xpath('//ul[@class="n-game cf"]/li/a/b/text()').extract()  #提取内容
        # print(txt)

        # 分块提取
        li_list = response.xpath('//ul[@class="n-game cf"]/li')
        for li in li_list:
            name = li.xpath('./a/b/text()').extract_first()  # extract_first() 相当于提取[0]，若无内容返回NONE
            variety = li.xpath('./em/a/text()').extract_first()
            date = li.xpath('./em/text()').extract_first()

            dic = {
                'name': name,
                'variety': variety,
                'date': date
            }

            # 通过yield将数据传给管道
            yield dic
