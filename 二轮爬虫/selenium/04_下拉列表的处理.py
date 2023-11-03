from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


web = Chrome()
web.get()

sel = web.find_element(By.XPATH,value='') #定位到下拉列表
sel_new = Select(sel)

#sel_new.options #可以获取下拉列表的所有选项
for i in range(len(sel_new.options)):
    sel_new.select_by_index(i) #通过索引选择选项
    #此时页面跳转后进行数据抓取
    # sel_new.select_by_value()  #根据value值选择选项
    # sel_new.select_by_visible_text() #根据选项标签内的文本选择选项























