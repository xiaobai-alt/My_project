import asyncio
import aiofiles
import aiohttp
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import pyWinhook as pyHook
import pythoncom  # 没这个库的直接pip install pywin32安装
import json
import requests
from lxml import etree
import base64
from urllib.parse import urljoin


def base64_api(uname, pwd, img_b64, typeid):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img_b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""


class Mouse():
    def funcLeft(self, event):
        if (event.MessageName != "mouse move"):  # 因为鼠标一动就会有很多mouse move，所以把这个过滤下
            print('左键点击')
        return True

    def main(self):
        # 创建管理器
        hm = pyHook.HookManager()
        # 监听鼠标
        # hm.MouseLeftDown 是将“鼠标左键按下”这一事件和func这个函数绑定，即每次鼠标左键按下都会执行func
        # 如果希望监测鼠标中键按下则：hm.MouseMiddleDown，鼠标右键按下则：hm.MouseRightDown
        hm.MouseLeftDown = self.funcLeft  # 监测鼠标左键是否按下
        if hm.HookMouse():
            # 循环监听
            pythoncom.PumpMessages()
        return True


def OpenChrome(url):
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('detach', True)
    web = Chrome(options=opt)
    web.get(url)
    script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
    web.execute_script(script)
    WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]')))
    web.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
    web.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/input').send_keys('1946162355@qq.com')
    web.find_element(By.XPATH, '/html/body/main/div/div[2]/div[1]/input').send_keys('chenhao#include0')
    web.find_element(By.ID, 'button').click()
    return web


def check_url(web):
    """
    url_to_be,用于通过检测首页url的方法来识别用户是否登录成功，
    current_handles,利用windows_handles方法获取当前页面窗口的权柄（窗口数量）
     通过等待判断用户是否打开新的窗口，借此获取用户想要下载的视频页面的url
    new_window_is_opened(current_handles)通过阅读源码可以发现，该方法在方法中再次获取当前窗口数，并与之前获取的窗口数（即我们传入的参数进行对比）
    会自动判别，返回真假。
    :param web:
    :return:
    """
    WebDriverWait(web, 1000, 2).until(EC.url_to_be('https://www.btnull.to/'))
    current_handles = web.window_handles
    WebDriverWait(web, 1000, 2).until(EC.new_window_is_opened(current_handles))
    web.switch_to.window(web.window_handles[-1])  # 切换到最后一个窗口
    now_url = web.current_url  # 获取当前页面url用做判断
    # 观察页面发现用户点击在线观看后不会新增窗口，因此根据url的变动作为判断依据
    WebDriverWait(web, 1000, 2).until(EC.url_changes(now_url))
    return web


def get_movie_url(web):
    try:
        resp = web.page_source
        tree = etree.HTML(resp)
        m3u8_url = \
            str(tree.xpath('/html/body/script[3]/text()')[0]).split("_BT.PC.player")[-1].strip(';').strip('()').strip(
                '{}').split(',')[0].split("'")[1]
        movie_name = \
            str(tree.xpath('/html/body/script[3]/text()')[0]).split("_BT.PC.player")[-1].strip(';').strip('()').strip(
                '{}').split(',')[2].split("'")[1]
    except:
        script1 = 'alert("获取失败，刷新中，若无反应请切换线路")'
        web.execute_script(script1)
        web.refresh()
    resp2 = requests.get(m3u8_url).text
    m3u8_2_url = urljoin(m3u8_url, str(resp2).split()[-1])
    return m3u8_2_url, movie_name


def down_m3u8(url, movie_name):
    resp = requests.get(url).text
    with open('./download_video/' + movie_name + 'm3u8.txt', mode='w', encoding='utf-8') as f:
        f.write(resp)
    print(movie_name, 'm3u8文件下载完成')


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
    login_url = 'https://www.btnull.to/user/login/'
    driver = OpenChrome(login_url)
    mouse = Mouse()
    driver = check_url(driver)
    movie_url, movie_name = get_movie_url(driver)
    down_m3u8(movie_url, movie_name)
    asyncio.run(down_all_ts(movie_url, movie_name))
