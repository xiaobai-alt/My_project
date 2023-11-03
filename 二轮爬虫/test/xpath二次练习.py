import requests
from lxml import etree

url = 'https://www.umei.cc/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
response_index = requests.get(url,headers=headers)
response_index.encoding='utf-8'

et_index = etree.HTML(response_index.text)

picture_kinds = et_index.xpath('//ul[@class="clearfix"]/li')
kinds = {}
for i in picture_kinds:
    name = i.xpath('./a/text()')[0]
    href = i.xpath('./a/@href')[0]
    kinds[name] = url.strip('/') + href
print(kinds.keys())
choice = str(input('请输入想要下载的图片类型：\n'))
picture_url = kinds[choice]
#print(picture_url)
response_picture_index = requests.get(picture_url,headers=headers)
response_picture_index.encoding='utf-8'

et_picture_kins = etree.HTML(response_picture_index.text)
next_picture_kinds_li = et_picture_kins.xpath('//div[@class="taotu-nav"]/span/h2')
pv = {}
for li in next_picture_kinds_li:
    kinds_name = li.xpath('./a/text()')[0]
    kinds_href = li.xpath('./a/@href')[0]
    pv[kinds_name] =  url.strip('/') + kinds_href
print(pv.keys())
choice2 = str(input("选择要下载的类型：\n"))
download_picture_url = pv[choice2]
#print(download_picture_url)

download_picture_response = requests.get(download_picture_url,headers=headers)
download_picture_response.encoding='utf-8'

tree = etree.HTML(download_picture_response.text)
picture_list = tree.xpath('//div[@class="item_list infinite_scroll"]/div')
#print(picture_list)
for li in picture_list:
    pic_name = li.xpath('./div//div[@class="img"]/a/img/@alt')[0] + '.jpg'
    pic_dw_url = li.xpath('./div//div[@class="img"]/a/img/@data-original')[0]
    filename = './test/' + pic_name
    response = requests.get(pic_dw_url,headers=headers).content
    with open(filename,mode='wb') as f:
        f.write(response)
        print('当前图片保存完成！')

print('全部下载完成')
# for li in picture_list:
#     name = li.xpath('./a/img/@alt')[0]
#     href_down = url.strip('/') + li.xpath('./a/@href')[0]
#     down_dict[name] = href_down
# print(down_dict.keys())
# choice3 = str(input('请输入完整的图片标题:\n'))
# download_url = down_dict[choice3]


# pic_list = tree.xpath('//div@[class="item_list infinite_scroll"]/div')
# for li in pic_list:
#     pic_name = li.xpath('./div[@class="img"]/a/img/@alt')[0] + '.jpg'
#     pic_dw_url = li.xpath('./div[@class="img"]/a/img/@src')[0]
#     filename = './test/' + pic_name
#     response = requests.get(pic_dw_url,headers=headers).content
#     with open(filename,mode='wb') as f:
#         f.write(response)
#         print('当前图片保存完成！')
#
# print('全部下载完成')









#
#
#
#
#

























































