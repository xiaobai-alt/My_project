import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def Query(info):
    baidu_url = 'https://www.baidu.com'
    web.get(baidu_url)
    query_btu = web.find_element(By.XPATH, '//*[@id="kw"]')
    query_btu.click()
    query_btu.send_keys(info, Keys.ENTER)

    time.sleep(2)  # 机房网络波动大，建议强制休眠等待页面反应，网络环境良好的可以去除此代码
    title = web.title
    return title


if __name__ == '__main__':
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('detach', True)
    web = Chrome(options=opt)
    query_info = '常州大学'
    Query(query_info)
    result = Query(query_info)
    print(result)
    time.sleep(10)
    web.close()
















