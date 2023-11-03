#_*_ coding:utf-8 _*_
# import requests
#
# url = 'http://img.daimg.com/uploads/allimg/221029/1-221029114J7.jpg'
# img_data = requests.get(url=url).content#content()返回二进制形式信息  text()返回字符串  json() 返回对象
#
# with open('./ceshi.jpg','wb') as fp:
#     fp.write(img_data)

#重点在二进制文件的存储，以及分页爬取

#尝试对大图网进行爬取http://www.daimg.com
#对银楼素材所有图片爬取
# import os.path
# import re
#
# import requests
# #创建一个文件夹用来保存图片
# if not os.path.exists('./hunshawang'):#判断是否存在该文件夹，不存在就新建
#     os.mkdir('./hunshawang')
# #UA伪装
# header = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
# }
#
# #分页爬取
# #设置一个通用url
# url = 'http://www.daimg.com/studio/wedding/list_8_%d.html'
# for pageNum in range(1,3):
#     #对应页面url
#     new_url = format(url%pageNum)
#     # 使用通用爬虫爬取首页信息
#     page_txt = requests.get(url=new_url, headers=header).text
#     #使用聚焦爬虫对
#     #分析图片连接所在源码位置，利用正则匹配
#     ev = '<a target="_blank" href.*? title.*?>.*?<img title.*? src="(.*?)" alt.*?</a>'
#     img_src_list = re.findall(ev,page_txt,re.S)
#     for src in img_src_list:
#         #存贮图片二进制信息
#         img_data = requests.get(url=src,headers=header).content
#         #生成图片名称,将网站后的图片原昵称截取下来
#         img_name = src.split('/')[-1]
#         #图片存储路径
#         imgPath = './hunshawang/' + img_name
#         with open(imgPath,'wb') as fp:  #wb存储二进制
#             fp.write(img_data)
#             print(img_name,'下载成功')

#bs4数据解析
# import requests
# from bs4 import BeautifulSoup
#
#
# #将本地的html文档中的数据加载到该对象中
# fp = open('./波晓张.html','r',encoding='utf-8')
# soup = BeautifulSoup(fp,'lxml')
# #print(soup.find('div',class_='vrwrap'))  #soup.（标签名） 返回的是html中出现的第一个标签
#
# print(soup.select('.text-layout>p span')[0].get_text())

#bs4实战
#需求：爬取三国演义小说中所有的章节标题和章节内容https://www.shicimingju.com/book/sanguoyanyi.html
# -*- coding:utf-8 -*-
# import requests
# from bs4 import BeautifulSoup
#
# if __name__ == '__main__':
#     url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
#         'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
#     }
#     page_txt = requests.get(url=url,headers=headers)
#     page_txt.encoding='utf-8' #获取数据乱码时，使用此方法
#     page_text = page_txt.text
#     #print(page_text)
#
#     #源码加载到对象
#     soup = BeautifulSoup(page_text,'lxml')
#     #解析章节标题和详情页url
#     list_mulu = []
#     b = soup.select('.book-mulu >ul > li')
#     fp = open('./三国.txt','w',encoding='utf-8')
#     for li in b:
#         title = li.a.string
#         debate_url = 'https://www.shicimingju.com'+li.a['href']
#         # print(title)
#         # print(debate_url)
#
#         #对详情页面发送请求，解析章节内容
#         detail_url_txt = requests.get(url=debate_url,headers=headers)
#         detail_url_txt.encoding='utf-8'
#         detail_url_text = detail_url_txt.text
#
#         #解析出详情页中相关的章节内容
#         detail_soup = BeautifulSoup(detail_url_text,'lxml')
#         div_tag = detail_soup.find('div',class_='chapter_content')
#         #解析获取章节内容
#         content = div_tag.text
#         fp.write(title+':'+content+'\n')
#         print(title,'爬取成功')

# from bs4 import BeautifulSoup
#
# import requests
# if __name__ == '__main__':
#     headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#
#         }
#     url = 'http://www.360doc.com/content/16/1004/11/502486_595674295.shtml'
#     page_txt = requests.get(url=url,headers=headers).text
#     soup = BeautifulSoup(page_txt,'lxml')
#     div_tag = soup.find('div',class_='article_container')
#     content = div_tag.text
#     with open('./test1.txt','w',encoding='utf-8') as fp:
#         fp.write(content)
#         print('下载完成')
#

#唐代诗人大全
# import requests
# from bs4 import BeautifulSoup
# if __name__ == '__main__':
#     url = 'https://www.gushimi.org/gushi/tangshisanbaishou/'
#     headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#
#             }
#
#     page_text = requests.get(url=url,headers=headers)
#     page_text.encoding='utf-8'
#     page_html = page_text.text
#
#     soup = BeautifulSoup(page_html,'lxml')
#
#     div_tag_list = soup.find_all('div',class_='news_box')
#     for li in div_tag_list:
#         title = li.a.string
#         print(title)


    #print(div_tag_list)


    # with open('./唐诗.txt','w',encoding='utf-8') as fp :
    #     fp.write(content)
    #     print('success')








#
# from lxml import etree
#
# if __name__ == '__main__':
#     parser = etree.HTMLParser(encoding='utf-8') #由于xpath对html规范严格，加入此语句可以避免报错
#     tree = etree.parse('唐诗.html',parser=parser)
#     #r = tree.xpath('/html//div')
#     # r = tree.xpath('//div[@class="news_box"]//text()')
#     r = tree.xpath('//div[@class="news_box"]/img/@lay-src')
#     print(r)

#xpath解析58二手房网https://cz.58.com/chuzu/


# import requests
# from lxml import etree
# if __name__ == '__main__':
#     #首先爬取整体页面信息
#     url = 'https://cz.58.com/chuzu/'
#     #UA伪装
#     headers = {
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#
#     page_text = requests.get(url=url,headers=headers).text
#
#     tree = etree.HTML(page_text)
#     li_list = tree.xpath('//ul[@class="house-list"]/li')
#     #print(li_list) #测试能否获取信息
#     fp = open('./58.txt','w',encoding='utf-8')
#     for li in li_list:
#         #局部获取页面数据
#         title = li.xpath('./div[2]/h2/a/text()')[0]
#         #print(title) #测试是否获取信息
#         price = li.xpath('./div[3]/div[2]/b/text()')[0]
#         fp.write(title+price+'\n')


#xpath联系：解析下载图片http://pic.netbian.com/4kmeinv/
# import requests
# from lxml import etree
# import os
# if __name__ == '__main__':
#     url = "http://pic.netbian.com/4kmeinv/"
#
#     headers = {
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#
#     page_txt = requests.get(url=url,headers=headers) #如果url指向的地址就是图片地址，此处用content
#     page_txt.encoding = 'gbk'
#     page_text = page_txt.text
#     #print(page_text)
#     #解析src属性值  alt属性值作为文件名
#     tree = etree.HTML(page_text)
#     li_list = tree.xpath('//ul[@class="clearfix"]/li')
#     #print(li_list)  #测试是否联通数据
#     if not os.path.exists('./oiclibs'):
#         os.mkdir('./piclibs')
#     for li in li_list:
#         img_name = li.xpath('./a/img/@alt')[0]+'.jpg'
#         #print(title)
#         img_src = "http://pic.netbian.com/4kmeinv/"+li.xpath('./a/img/@src')[0]
#         #print(new_url)
#
#         img_data = requests.get(url=img_src,headers=headers).content
#         img_path = 'piclibs/'+img_name
#         with open(img_path,'wb') as fp:
#             fp.write(img_data)
#             print('保存成功')





































