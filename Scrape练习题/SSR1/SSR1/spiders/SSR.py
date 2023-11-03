import scrapy
from urllib.parse import urljoin
from SSR1.items import Ssr1Item


class SsrSpider(scrapy.Spider):
    name = "SSR"
    allowed_domains = ["ssr1.scrape.center"]
    start_urls = ["https://ssr1.scrape.center/"]

    def parse(self, response):
        div_list = response.xpath('/html/body/div/div[2]/div[1]/div[1]/div')
        for div in div_list:
            href = urljoin(response.url, div.xpath('./div/div/div[2]/a/@href').extract_first())
            yield scrapy.Request(
                url=href,
                method='get',
                callback=self.parse_next
            )
        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(
                url=response.urljoin(next_url),
                callback=self.parse
            )

    def parse_next(self, resp):
        print(resp.url, '请求成功')
        movie_name = resp.xpath('/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()').extract_first()
        movie_type_list = resp.xpath(
            '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]//button//span//text()').extract()
        movie_type = ''
        for i in range(len(movie_type_list)):
            movie_type += movie_type_list[i]
            movie_type += '-'
        movie_p_type = movie_type.rstrip('-')
        movie_area_list = resp.xpath(
            '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[2]//span//text()').extract()
        movie_area = ''
        for i in range(len(movie_area_list)):
            movie_area += movie_area_list[i]
        movie_time = resp.xpath(
            '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()').extract_first()
        if not movie_time:
            movie_time = '未找到上映时间'
        movie_score = resp.xpath(
            '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()').extract_first().strip('\n').strip()
        # movie_detail = resp.xpath(
        #     '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()').extract_first().strip(
        #     '\n').strip().replace("''", '')
        movie_detail = resp.xpath(
            '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()').extract_first().strip(
            '\n').lstrip()

        item = Ssr1Item()
        item['movie_name'] = movie_name
        item['movie_type'] = movie_p_type
        item['movie_area'] = movie_area
        item['movie_time'] = movie_time
        item['movie_score'] = movie_score
        item['movie_detail'] = movie_detail.replace('\n', '').rstrip()
        print(item)
        yield item
