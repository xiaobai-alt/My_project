import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ErshoucheSpider(CrawlSpider):
    name = "ershouche"
    allowed_domains = ["che168.com","autohome.com.cn"]
    start_urls = ["https://www.che168.com/nlist/beijing/list/?pvareaid=100533"]

    rules = (  # rule规则，在此处定义了一堆规则，要求必须是元组或列表
        # Rule：规则对象
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='goodStartSolrQuotePriceCore0']/ul/li/a",)), callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='listpagination']/a",)), follow=True)
    )

    # 此处需要注意，不能在该末班中自定义parse方法，parse由CrawlSpider提供
    def parse_item(self, response):
        title = response.xpath("//div[@class='car-box']/h3//text()").extract_first()
        price = response.xpath("//span[@id='overlayPrice']//text()").extract_first()
        print(title, price)
