import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

urls = [
    'https://test1.rar',
    'https://test2.rar',
    'https://test3.rar'
]

def get_content(url):
    print('正在爬取：',url)
    #在实验过程中发现get是一个阻塞的方法
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        return response.content
def parse_content(content):
    print('响应数据的长度是：',len(content))

for url in urls:
    content = get_content(url)
    parse_content(content)