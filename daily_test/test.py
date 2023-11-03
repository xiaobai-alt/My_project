import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
opt.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
opt.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面

opt.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
web = Chrome(options=opt)
# web.get('https://www.baidu.com')
web.get('https://www.xiaohongshu.com/login')
# # 解除浏览器特征识别selenium
script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
web.execute_script(script)
# web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })

time.sleep(10000)
