from selenium import webdriver

import time

bro  = webdriver.Firefox(executable_path='./geckodriver')

bro.get('https://www.taobao.com')

#标签定位：
bro.find_element(by='id',value='q').send_keys('Iphone')

#执行一组js程序
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
time.sleep(2)
#标签交互
#search_input.send_keys('Iphone')
bro.find_element(by='class name',value='btn-search').click()

#btn.click()
bro.get('https://www.baidu.com')
time.sleep(2)
#回退
bro.back()
time.sleep(2)
bro.forward()

time.sleep(5)
bro.quit()













