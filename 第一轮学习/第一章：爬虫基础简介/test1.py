#实战一：需求：爬取搜狗首页的页面数据
#encoding='utf-8'
#import requests
# if __name__ =="__main__":
#     """
#     url: 需要爬取的网站地址
#     response:响应对象
#     page_txt:响应数据体
#     sougou.html:保存的文件名称
#     """
#     url = "https://www.sogou.com/"
#     response = requests.get(url=url)
#     page_txt = response.text
#     print(page_txt)
#     #持久化存储
#     with open('./sougou.html','w',encoding='utf-8') as fp:
#         fp.write(page_txt)
#     print("爬取结束")


#练习2：爬取搜狗指定词条对应的搜索结果页面（简易的网页采集器）
# import requests
# if __name__ == "__main__":
#     #UA伪装：将对应的User-Agent封装到一个字典中
#     """
#     url:要爬取的搜狗网址
#     kw:处理url中携带的参数，使其变为动态的：封装到字典中
#     page_text:页面数据
#     filename:将要保存的文件名
#     """
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#     url = "https://www.sogou.com/web"
#     # 使其参数动态化，方便操作
#     kw = input('enter a word：')
#     param = {
#         'query':kw
#     }
#     page_text = requests.get(url=url,params=param,headers=headers).text
#     filename = kw+'.html'
#     with open(filename,'w',encoding='utf-8') as fp:
#         fp.write(page_txt)
#     print(filename,'保存成功')

#案例3 ：破解百度翻译  此时要爬取的不是整个页面，而是翻译过后的词汇的特定信息

#由于此类网站在输入词条后进行局部更新，所以我们要看网页后台的ajex（交互），网络模块中XHR对应的就是ajex
#通过实时输入参数，检测network中刷新的XHR中的sug，当sug携带的请求为完整数据时，查看其url及携带的参数，并查看请求方式是POST还是GET

# import requests
# import json
# if __name__ == '__main__':
#     """
#     post_url:目标网址
#     word:要翻译的参数
#     filename:保存文件名
#     """
#     header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
#     }
#     post_url = 'https://fanyi.baidu.com/sug'
#
#     word = input('enter a word:')
#     #post请求参数处理，相当于get中的param
#     data = {
#         'kw':word
#     }
#     dic_obj = requests.post(url=post_url,data=data,headers=header).json()
#     #json()方法返回的是一个obj，只有在确实响应数据时json类型时才可以使用 即conten-type:json
#     filename = word+'.json'
#     fp = open(filename,'w',encoding='utf-8')
#     json.dump(dic_obj,fp=fp,ensure_ascii=False)#ensure_ascii=False因为中文不能转换ascii
#     print('Over')

#案例4：爬取豆瓣电影详细数据

# import requests
# import json
#
# url = 'https://movie.douban.com/j/chart/top_list?type=24&interval_id=100:90&action=&start=20&limit=20'
# header = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
# }
# param = {
#     'type':'24',
#     'interval_id':'100:90',
#     'action':'',
#     'start':'20', #从库中第几部电影开始取
#     'limit':'20', #一次取得的个数
# }
# list_data = requests.get(url=url,params=param,headers=header).json()
# fp = open('./douban.json','w',encoding='utf-8')
# json.dump(list_data,fp=fp,ensure_ascii=False)
# print('ovwr')

#作业：爬取肯德基餐厅查询 https://www.kfc.com.cn/kfccda/index.aspx
# import requests
# import json
#
# url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
# keyword1 = input('enter adress:')
# data = {
#     'cname':'',
#     'pid':'',
#     'keyword':keyword1, #此处若将keyword1加引号，会导致空列表
#     'pageIndex':'1',
#     'pageSize':'10'
# }
# header = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
# }
# page_text = requests.post(url=url,data=data,headers=header).text()
# with open('./kfc.txt','w',encoding='utf-8') as fp:
#     fp.write(page_txt)
#
# # dic_data = response.json()
# # fp = open('./kfc.json','w',encoding='utf-8')
# # json.dump(dic_data,fp=fp,ensure_ascii=False)
#
# print('over')

# 案例4 药监总局
#
# import requests
# import json
# url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'  #url已经无法使用
# header = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
# }
# data ={
# 	"on": "true",
# 	"page": "1",
# 	"pageSize": "15",
# 	"productName": "",
# 	"conditionType": "1",
# 	"applyname": "",
# 	"applysn": ""
# }
# id_list = []
# json_ids = requests.post(url=url,data=data,headers=header).json()
# for dic in json_ids('[list]'):
#     id_list.append(dic['ID'])
# print(id_list)


#练习：爬取笔趣阁
# import requests
#
# url = 'http://www.biqu5200.net/147_147321/'
# header = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
# }
# page_txt = requests.get(url=url,headers=header).text
# with open('./万相之王.txt','w',encoding='utf-8') as fp:
#     fp.write(page_txt)
# print('Over')









