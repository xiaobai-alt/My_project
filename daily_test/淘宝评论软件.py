import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


def web_create():
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
    opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
    web = Chrome(options=opt)
    web.get('https://kyfw.12306.cn/otn/resources/login.html')
    # 解除浏览器特征识别selenium
    script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
    web.execute_script(script)
    return web


def user_info():
    info_dic = {
        'user': '13295151779',
        'password': 'chenhao#include0'

    }
    return info_dic


def login(username, password):
    web.get(
        'https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.754894437.1.5af92a89avZqQZ&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F')
    web.refresh()
    web.find_element(By.ID, 'fm-login-id').click()
    web.find_element(By.ID, 'fm-login-id').send_keys(username)
    web.find_element(By.ID, 'fm-login-password').click()
    web.find_element(By.ID, 'fm-login-password').send_keys(password)
    web.find_element(By.XPATH, '//*[@id="login-form"]/div[4]').click()

    time.sleep(3)
    web.switch_to.frame('baxia-dialog-content')
    WebDriverWait(web, 5, 1).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/center/div[1]/div/div/div/div[2]')))

    span = web.find_element(By.XPATH, '/html/body/center/div[1]/div/div/div/div[2]')

    action = ActionChains(web)
    action.click_and_hold(span).move_by_offset(140,
                                               0).perform()  # click_and_hold代表点击并保持点击动作。move_by_offset(x, y)，其中x代表水平移动距离，y代表垂直移动距离


    web.switch_to.default_content()
    web.find_element(By.XPATH, '//*[@id="login-form"]/div[4]').click()

if __name__ == '__main__':
    web = web_create()
    user_information = user_info()
    login(user_information['user'], user_information['password'])
