import requests
from lxml import etree


url = 'https://suqian.zbj.com/search/service/?kw=saas&r=2'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
response = requests.get(url,headers=headers)
response.encoding='utf-8'

tree = etree.HTML(response.text)

div_list = tree.xpath('//div[@class="search-result-list-service search-result-list-service-width"]/div')

for li in div_list:
    price = li.xpath('./div//div[@class="price"]/span/text()')
    if not price:
        continue
    price = price[0]
    sorce = li.xpath('./div//div[@class="fraction"]/span[1]/text()')
    if not sorce:
        continue
    sorce = sorce[0]
    name = li.xpath('./div//div[@class="name-pic-box"]/a//text()')
    if not name:
        continue
    name = ''.join(name)
    company = li.xpath('./div//div[@class="shop-info text-overflow-line"]/text()')[0]
    print('软件名称:'+name,'开发价格:'+price,'评价:'+sorce,'公司:'+company)