
import  requests
url = 'http://www.baidu.com/s?wd=ip'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
}
page_text = requests.get(url=url,headers=headers,proxies={'http':'117.114.149.66'})
page_text.encoding = 'utf-8'
page_index_text = page_text.text

with open('ip.html','w',encoding='utf-8') as fp:
    fp.write(page_index_text)