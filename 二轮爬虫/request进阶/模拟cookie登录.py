#对17小说网进行爬取
#1登录  》 得到cookie，带着cookie，请求url书架  》 书架上的内容
#利用session进行cookie保存

import requests


Session = requests.session()

def login_index_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    data = {
        'loginName': '13295151779',
        'password': 'chenhao#include0'
    }
    Session.post(url,data=data,headers=headers)
    #print(response.cookies)
    response = Session.get('https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919')
    print(response.json())


def main():
    url = 'https://passport.17k.com/ck/user/login'
    login_index_page(url)
if __name__ == '__main__':
    main()




































