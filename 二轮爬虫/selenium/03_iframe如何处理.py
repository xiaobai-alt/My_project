from selenium.webdriver import Chrome
web =Chrome()
from selenium.webdriver.common.by import By

#要想提取到iframe中的内容需要先切换到iframe窗口中
iframe = web.find_element(By.XPATH,value='')
web.switch_to.frame(iframe) #切换到窗口中



#获取数据后可以退出iframe窗口到原窗口接着提取其余信息
web.switch_to.parent_frame() #该命令直接切除iframe窗口




































