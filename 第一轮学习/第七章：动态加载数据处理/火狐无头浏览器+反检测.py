from selenium import webdriver
from time import sleep


#实现无可视化界面selenium规避检测
from selenium.webdriver import FirefoxOptions

#实现无可视化界面的操作
#实例化一个options对象
firefox_options = FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')

#实现规避检测
#firefox_options.add_argument('--disable-blink-features=AutomationControlled')

#如何实现selenium规避被检测的风险
bro = webdriver.Firefox(executable_path='./geckodriver',options=firefox_options)

#无可视化界面
bro.get('https://www.baidu.com')

print(bro.page_source)

sleep(2)
bro.quit()









