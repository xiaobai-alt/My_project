import json

import requests
from lxml import etree

def index_response(url):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        for current in range(5):
            data = {

                    "limit": "20",
                    "current": current,
                    "pubDateStartTime": "",
                    "pubDateEndTime": "",
                    "prodPcatid": "",
                    "prodCatid": "",
                    "prodName": ""

            }
        response = requests.post(url,data=data,headers=headers,timeout = 10).text
        tree = etree.HTML(response)

        print(response)
        # content = json.loads(response)
        # print(type(content))


        # list = response['list']
        # with open('./菜价.txt',mode='a',encoding='utf-8') as f:
        #     for i in range(len(list)):
        #         f.write(str(list[i]))
        #         f.write('\n')

if __name__ == '__main__':
    url = 'http://www.xinfadi.com.cn/getPriceData.html'
    index_response(url)








































