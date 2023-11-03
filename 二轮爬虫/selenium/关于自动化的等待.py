#第一种，使用time.sleep()睡眠,无论数据是否加载，都会睡眠等待

#第二种 implicitly_wait() #可能提前被唤醒的睡眠，最长等待时间自己设置  全局设置，设置完全局都有效，最常用

#


from selenium.webdriver import Chrome
#显示等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree




def get_page_source():
    web.get(url)

    el = WebDriverWait(web,10,0.5).until(  #until 结束等待的条件  。该语句的意思是等待10秒，每0.5秒查看下状态，直到web内容请求到
        EC.presence_of_element_located(By.XPATH,'')
    )
    return web.page_source

def get_job_name(page_source):
    tree = etree.HTML(page_source)
    job_names = tree.xpath()

if __name__ == '__main__':
    web = Chrome()
    url = 'http://www.lagou.com'
    get_page_source(url)





































