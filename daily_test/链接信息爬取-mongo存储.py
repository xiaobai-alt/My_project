import requests
from lxml import etree
from MongoDB链接操作 import add_many


def get_page_source(url):
    resp = requests.get(url).text
    return resp


def get_info_list(page_source):
    tree = etree.HTML(page_source)
    ul_list = tree.xpath('//*[@id="content"]/div[1]/ul/li')
    # print(ul_list)
    result = []
    for li in ul_list:
        title = li.xpath('./div[@class="info clear"]/div[@class="title"]/a/text()')[0]
        flood_list = li.xpath('./div[@class="info clear"]/div[@class="flood"]/div/a/text()')
        flood = '-'.join(flood_list).replace(" ", "")
        address = li.xpath('./div[@class="info clear"]/div[@class="address"]//text()')[0]
        follow_info = li.xpath('./div[@class="info clear"]/div[@class="followInfo"]//text()')[0]
        price_list = li.xpath('./div[@class="info clear"]/div[@class="priceInfo"]//text()')
        price = ''.join(price_list)
        dic = {
            'title': title,
            'flood': flood,
            'address': address,
            'follow_info': follow_info,
            'price': price
        }
        result.append(dic)
    return result


def save_by_mongo(info_list):
    result = add_many('ershoufang', info_list)
    print(result)


if __name__ == '__main__':
    for i in range(1, 5):
        index_url = f'https://changzhou.lianjia.com/ershoufang/pg{i}/'
        source = get_page_source(index_url)
        data_list = get_info_list(source)
        save_by_mongo(data_list)
