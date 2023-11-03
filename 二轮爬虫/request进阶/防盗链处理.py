#1.首先获取contid
#2.拿到videoStatus返回的json 》srcUrl
#3.对url进行整理拼接
#4.下载视频


import requests


url = 'https://www.pearvideo.com/video_1776862'

conId = url.split('_')[1]

videoStatusurl = f'https://www.pearvideo.com/videoStatus.jsp?contId={conId}&mrd=0.20319670400647238'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    #防盗链：溯源，查询当次请求的上一级
    'Referer': 'https://www.pearvideo.com/video_1776862'
}

response = requests.get(videoStatusurl,headers=headers)
srcurl = response.json()['videoInfo']['videos']['srcUrl']
systemTime = response.json()['systemTime']
srcurl = srcurl.replace(systemTime,f'cont-{conId}')
video = requests.get(srcurl).content
#print(srcurl)
with open('./test.mp4',mode='wb') as f:
    f.write(video)
    print('下载完成')



























