#_*_ coding:utf-8 _*_
import requests
from lxml import etree
import os

if __name__ == '__main__':
    #由于网址较多，要定义好每个页面的网址名称
    """
    all_variety_url_list : 小说分类列表
    variety_name：分类名称
    variety_name_list：分类名称列表
    variety_url_dict：分类名称及对应的链接地址
    """
    index_url = 'https://www.bqg99.com/'
    #防止页面反爬虫，UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    }
    index_page_text = requests.get(url=index_url,headers=headers).text
    #print(index_page_text)
    tree = etree.HTML(index_page_text)
    #快速定位到小说分类
    all_variety_url_list = tree.xpath('//div[@class="header"]/div[2]/ul/li')
    #print(all_variety_url_list)
    if not os.path.exists('./novel_download'):
        os.mkdir('./novel_download')

    #做好分类网址统计
    variety_url_dict = {}
    variety_name_list = []
    for li in all_variety_url_list:
        variety_name = li.xpath('./a/text()')[0]
        variety_name_list.append(variety_name)
        #print(variety_name)
        variety_url = 'https://www.bqg99.com' + li.xpath('./a/@href')[0]
        variety_url_dict[variety_name] = variety_url
    #print(variety_url_dict)
    #为了让读者快速选择想要搜索的分类
    print(variety_name_list)
    download_variety_name = str(input("请输入上面列表想要查询的小说分类：\n"))
    while (download_variety_name is not None):
        if (download_variety_name in variety_name_list):
            """
            novel_name_div_list：小说名称所在div的列表集合
            novel_name_list :小说名称列表
            
            """
            print('马上为您返回结果\n')
            variety_url = variety_url_dict[download_variety_name]
            #print(variety_url)
            variety_page_text = requests.get(url=variety_url,headers=headers).text
            #观测页面发现item列表是随着鼠标移动实时刷新的
            tree1 = etree.HTML(variety_page_text)
            novel_name_div_list = tree1.xpath('//div[@class="hot"]/div')
            #print(novel_name_div)
            novel_name_url_dict = {}
            novel_name_list = []
            for div in novel_name_div_list:
                novel_name = div.xpath('./dl/dt/a/text()')[0]
                novel_name_list.append(novel_name)
                #print(novel_name)
                novel_url = 'https://www.bqg99.com' + div.xpath('./dl/dt/a/@href')[0]
                #print(novel_url)
                novel_name_url_dict[novel_name] = novel_url
            print(novel_name_list)
            download_novel_name = str(input("请从上列表中选择要下载的小说：\n"))

            #为了预防输入错误信息，加入while循环来检测输入信息
            while (download_novel_name is not None) :
                if (download_novel_name in novel_name_list):
                    """
                    novel_download_name : 想要下载的小说名
                    downloa_url ： 小说链接
                    novel_listmain ：小说章节列表
                    """
                    print("马上为您下载。")
                    novel_download_name = download_novel_name + '.txt'
                    novel_path = './novel_download/' + novel_download_name
                    fp =  open(novel_path,'w',encoding='utf-8')
                    print(novel_download_name)
                    downloa_url = novel_name_url_dict[download_novel_name]
                    #print(downloa_url)

                    download_novel_text = requests.get(url=downloa_url,headers=headers).text
                    tree2 = etree.HTML(download_novel_text)
                    #小说详细章节列表做好统计
                    novel_listmain = tree2.xpath('//div[@class="listmain"]/dl/dd | //div[@class="listmain"]/dl/span/dd')
                    novel_list = list(novel_listmain)
                    novel_list.pop(10)
                    #print(novel_list)
                    novel_sousuo_name_dick = {}

                    for li in novel_list:
                        """
                        title : 小说具体章节名
                        novel_sousuo_href ：小说具体章节对应的链接
                        download_text_content:小说原文所在列表
                        string_text：小说原文
                        """

                        title = li.xpath('./a/text()')[0]
                        #novel_sousuo_name_list.append(novel_sousuo_name)
                        novel_sousuo_href = 'https://www.bqg99.com' + li.xpath('./a/@href')[0]
                        #novel_sousuo_name_dick[novel_sousuo_name] = novel_sousuo_href

                        download_text = requests.get(url=novel_sousuo_href,headers=headers).text
                        #print(download_text)
                        tree3 = etree.HTML(download_text)
                        download_text_content = tree3.xpath('//div[@class="Readarea ReadAjax_content"]/text()')
                        #print(download_text_content)
                        #break
                        string_text = ""
                        for i in range(len(download_text_content)):
                            #string_text = "".join(str(download_text_content[i]))
                            string_text = string_text+str(download_text_content[i])+'\n'
                        #print(title+'\n'+string_text+'\n')
                        fp.write(title+'\n'+string_text+'\n')
                        print(title+'下载成功')



                            #print(string_text)
                            # s_replace = string_text.replace('<br>','\n')
                            # while True:  # 用换行符替换所有的'<br/>'
                            #     index_begin = s_replace.find("<")
                            #     index_end = s_replace.find(">", index_begin + 1)
                            #     if index_begin == -1:
                            #         break
                            #     s_replace = s_replace.replace(s_replace[index_begin:index_end + 1], "")

                        #print(s_replace)

            else:
                print('检测失败，请输入正确的小说名称\n')
                download_novel_name = str(input())
    else:
        print('检测失败，请输入正确的分类名称')
        download_variety_name = str(input("请输入上面列表想要查询的小说分类：\n"))
