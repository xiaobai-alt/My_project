import scrapy
from scrapy.linkextractors import LinkExtractor  # 链接提取器


class ErshouSpider(scrapy.Spider):
    name = "ershou"
    allowed_domains = ["che168.com", "autohome.com.cn"]
    start_urls = ["https://www.che168.com/nlist/beijing/list/?pvareaid=100533"]

    def parse(self, response):
        #  普通爬虫的逻辑
        # li_list = response.xpath('//*[@id="goodStartSolrQuotePriceCore0"]/ul/li')
        # for li in li_list:
        #     title = li.xpath('./a/div[2]/h4/text()').extract_first()
        #     href = li.xpath('./a/@href').extract_first()
        #     yield scrapy.Request(
        #         url=response.urljoin(href),
        #         callback=self.parse_detail
        #
        #     )

        # 新逻辑 scrapy 提供了链接提取器，可以方便我们提取页面中的超链接
        le = LinkExtractor(restrict_xpaths=('//*[@id="goodStartSolrQuotePriceCore0"]/ul/li/a',))
        links = le.extract_links(response)  # 提取页面的链接
        for link in links:
            # print(link.text.replace(" ", ""), link.url)
            yield scrapy.Request(
                url=link.url,
                callback=self.parse_detail
            )

        page_link = LinkExtractor(restrict_xpaths=("//div[@id='listpagination']/a",))
        page_list = page_link.extract_links(response)  # 提取分页url
        for page in page_list:
            yield scrapy.Request(
                url=page.url,
                callback=self.parse
            )

    def parse_detail(self, resp):
        print(resp.url)
