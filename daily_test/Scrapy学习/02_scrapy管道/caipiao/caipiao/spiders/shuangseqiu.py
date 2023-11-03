import scrapy
from caipiao.items import CaipiaoItem


class ShuangseqiuSpider(scrapy.Spider):
    name = "shuangseqiu"
    allowed_domains = ["500.com"]
    start_urls = ["https://datachart.500.com/ssq/"]

    def parse(self, response, **kwargs):
        trs = response.xpath('//tbody[@id="tdata"]/tr')
        for tr in trs:
            if tr.xpath('./@class').extract_first() == 'tdbck':
                continue
            num = tr.xpath('./td[1]/text()').extract_first().strip()
            red_boll = tr.xpath('./td[@class="chartBall01"]/text()').extract()
            # scrapy支持xpath与css混合使用
            blue_boll = tr.css('.chartBall02::text').extract_first()

            cai = CaipiaoItem()  # 此步相当于定义了一个字典，但是key值是写死的，无法改变，避免了后续引用出错的问题
            cai['qihao'] = num
            cai['red_boll'] = red_boll
            cai['blue_boll'] = blue_boll

            yield cai
            # 原先的存储时自定义一个自带你，但这种方法很可能导致后续修改参数名时报错，不易找到自己定义的内容，因此scrapy提供了items供使用者定义其字典
            # dic = {
            #     'qihao': num,
            #     'red_boll': red_boll,
            #     'blue_boll': blue_boll
            # }
            #
            # yield dic
