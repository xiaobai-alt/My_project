# -*- coding:utf-8 -*-
#项目需求：解析出全国城市名称https://www.aqistudy.cn/historydata/

# import requests
# from lxml import etree
# if __name__ == "__main__":
#
#     url = "https://www.aqistudy.cn/historydata/"
#
#     #为了防止页面检测非人为访问，进行UA伪装
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#
#     page_text = requests.get(url=url,headers=headers).text
#
#     tree = etree.HTML(page_text)
#
#     # hot_city_list = tree.xpath('//div[@class="bottom"]/ul/li')
#     # all_city_name = []
#     # #解析到热门城市名称
#     # for li in hot_city_list:
#     #     hot_city_name = li.xpath('./a/text()')[0]
#     #     all_city_name.append(hot_city_name)
#     #
#     # #解析全部城市名称
#     # city_names_list = tree.xpath('//div[@class="bottom"]/ul/div[2]/li')
#     # for li in city_names_list:
#     #     city_name = li.xpath('./a/text()')[0]
#     #     all_city_name.append(city_name)
#     #
#     # print(all_city_name,'\n',len(all_city_name))
#
#     a_list = tree.xpath('//div[@class="bottom"]/ul/li | //div[@class="bottom"]/ul/div[2]/li')
#     all_city_names = []
#     for li in a_list:
#         city_name = li.xpath('./a/text()')[0]
#         all_city_names.append(city_name)
#     print(all_city_names,'\n',len(all_city_names))


#z作业：爬取战长素材免费模板
# import requests
# from lxml import etree
# import os
# if __name__ == '__main__':
#     url = 'https://aspx.sc.chinaz.com/query.aspx'
#     param = {
#         'keyword' : '免费简历'
#     }
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#
#     page_text = requests.get(url=url,params=param,headers=headers).text
#     #print(page_text)
#     tree = etree.HTML(page_text)
#
#     all_content_list = tree.xpath('//div[@class="new_block"]')[0:10]
#     #print(all_content_list)
#     data_href_list = []
#     for li in all_content_list:
#         data_href = li.xpath('./div[1]/a/@href')[0]
#         #print(data_href)
#         data_href_list.append(data_href)
#     #print(data_href_list)
#     if not os.path.exists('./download'):
#         os.mkdir('./download')
#     for url in data_href_list:
#         data_url = url
#
#         #请求下载页面
#         new_page_txt = requests.get(url=url,headers=headers)
#         new_page_txt.encoding = "utf-8"
#         new_page_text = new_page_txt.text
#         #print(new_page_text)
#         tree1 = etree.HTML(new_page_text)
#
#         download_url_list = tree1.xpath('//div[@class="clearfix mt20 downlist"]/ul/li')[0:1]
#
#         for li in download_url_list:
#             download_url = li.xpath('./a/@href')[0]
#             download_content = requests.get(url=download_url,headers=headers).content
#
#             download_content_name = li.xpath('./a/text()')[0] + '.rar'
#             download_content_rar = 'download/' + download_content_name
#             with open(download_content_rar,'wb') as fp:
#                 fp.write(download_content)
#             print('下载完成')
#             #print(download_url)


































