from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opt = Options()
opt.add_experimental_option('detach', True)  # 运行完不关闭窗口
opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置开发者模式启动 ，模拟真正的浏览器
web = Chrome(options=opt)
# 解除浏览器特征识别selenium
script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
web.execute_script(script)


web.get('https://kyfw.12306.cn/otn/resources/login.html')
