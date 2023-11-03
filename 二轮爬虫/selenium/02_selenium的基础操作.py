# 目标：拉勾网的招聘信息
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys #模拟键盘按键的包
from selenium.webdriver.common.by import By
import time

web = Chrome()
web.get("http://www.lagou.com")

# 找到页面上的定位城市，并点击
x_btn = web.find_element(by='id' ,value='cboxClose')
x_btn.click()

time.sleep(1)  # 模仿人的行为，进行延迟处理
# 在搜索框输入要查询的信息，并进行点击
in_put = web.find_element(by='id' ,value='search_input').send_keys('python',Keys.ENTER)

time.sleep(1)
# 导入By包，可以通过xpath等标签提取数据
li_list = web.find_elements(By.XPATH, value='//*[@id="openWinPostion"]')

# selenium可以动态执行js，可以借此删除页面上一些不需要的阻碍数据爬取的内容
# web.execute_script("""
#     var a = document.getElementsByClassName("");
#     a.parentNode.removeChild(a);
# """)

for li in li_list:
    li.click()
    # 点击命令后页面会跳转到新的页面，此时需要通过selenium同样跳转到新窗口web.window_handles指页面所有窗口的列表
    web.switch_to.window(web.window_handles[-1])  # [-1]列表最后一项默认新窗口
    content = web.find_element(By.XPATH,value='//*[@id="job_detail"]/dd[2]')
    print(content.text)
    time.sleep(1)
    # 获取数据后关闭窗口，调整selenium视角，接着爬取下一条
    web.close()
    web.switch_to.window(web.window_handles[0])
    




















