import asyncio
from urllib.parse import urljoin
import aiohttp
import aiofiles


async def down_one_ts(url, movie_name):
    while 1:
        try:
            filename = url.split('/')[-1].strip()
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.content.read()
                    async with aiofiles.open(f'./download_video/{movie_name}/' + filename, mode='wb') as f:
                        await f.write(data)
            print(url + '下载完成')
            break
        except:
            print('正在刷新' + url)
            await asyncio.sleep(2)


async def down_all_ts(url, movie_name):
    tasks = []
    with open('./download_video/' + movie_name + 'm3u8.txt', mode='r', encoding='utf-8') as f:
        for li in f:
            if li.startswith('#'):
                continue
            else:
                down_url = urljoin(url, li)
                task = asyncio.create_task(down_one_ts(down_url, movie_name))
                tasks.append(task)
    await asyncio.wait(tasks)


if __name__ == '__main__':
    url = 'https://vip.ffzy-online6.com/20230704/14433_0f6a0142/2000k/hls/index.m3u8'
    movie_name = '若虫：森林之歌'
    asyncio.run(down_all_ts(url, movie_name))
