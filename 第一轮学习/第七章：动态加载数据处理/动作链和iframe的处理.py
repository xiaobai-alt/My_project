from selenium import webdriver
import time
#导入动作链对应的类
from selenium.webdriver import ActionChains


bro = webdriver.Firefox(executable_path='./geckodriver')

bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')


#如果定位到的标签实在iframe标签之中的则必须通过下面操作在进行标签定位
bro.switch_to.frame('iframeResult') #切换浏览器标签定位的作用域
div = bro.find_element(by='id',value='draggable')

#动作链
action = ActionChains(bro)

#点击长按指定的标签
action.click_and_hold(div)
for i in range(5):
    #perform()立即执行动作链操作
    action.move_by_offset(40,0).perform() #内部值是一次偏移的像素.数值正右负左,并且move_by_offset(x,y)有两个参数（x,y）x代表水平方向，y代表垂直方向
    time.sleep(0.3)

#释放动作链
action.release()
div.click()
time.sleep(5)

bro.quit()





















