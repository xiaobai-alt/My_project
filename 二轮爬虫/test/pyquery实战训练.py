#目标网站https://www.umei.cc/  获取最新更新的图片内容
import requests
from pyquery import PyQuery
from lxml import etree
#创建获取页面源码的方法
def get_page_sourse(url):
    response = requests.get(url)
    response.encoding='utf-8'
    #print(response.text)
    return response.text

#创建分析页面源码的方法
def parse_page_sourse(html):
    doc = PyQuery(html)
    list = doc(".sliderbox dt").items()
    #print(list)
    new_pic_dict = {}
    for li in list:
        title = li("span.title a").text().replace('<span>','').replace('</span>','')
        href = 'https://www.umei.cc' + li("span.title a").attr("href")
        #print(title,'\n',href)
        new_pic_dict[title] = href
    #print(new_pic_dict)
    return new_pic_dict
#创建图片下载方法
def down_pic(new_pic_dict):
    url_list = []
    for value in new_pic_dict.values():
        #print(value)
        url_list.append(value)
    #print(url_list)
    for i in range(len(url_list)):
        filename = './test_daily/' + list(new_pic_dict.keys())[i] +'.jpg'
        response = requests.get(url_list[i])
        response.encoding='utf-8'
        tree = etree.HTML(response.text)
        pic_url = tree.xpath('//div[@class="big-pic"]/a/img/@src')[0]
        response1 = requests.get(pic_url).content

        with open(filename,mode='wb') as f:
            f.write(response1)
            print('图片下载完成')
    print('下载完成')
def main():
    # 1.提取页面源代码
    # 2.解析页面源码，获取数据
    url = 'https://www.umei.cc/'
    html = get_page_sourse(url)
    new_pic_dict = parse_page_sourse(html)
    down_pic(new_pic_dict)

if __name__ == '__main__':
    main()



































