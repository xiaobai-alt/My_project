
#1.尝试selenium
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


def login(user,password):
            while 1:
                    try:
                        url = 'https://www.damai.cn/'
                        web.get(url)
                        web.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[1]/span').click()
                        break
                    except StaleElementReferenceException:
                        web.refresh()
            # 点击密码登录
            # WebDriverWait(web,10,0.5).until(EC.url_to_be('https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F'))
            #web.switch_to.frame('alibaba-login-box')
            iframe = web.find_element(By.TAG_NAME,'iframe')[0]
            web.switch_to.frame(iframe)
            WebDriverWait(web, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-tabs"]/div[1]')))
            web.find_element(By.XPATH, '//*[@id="login-tabs"]/div[1]').click()
            web.find_element(By.XPATH, '//*[@id="fm-login-id"]').click()
            web.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(user)

            web.find_element(By.XPATH, '//*[@id="fm-login-password"]').click()

            web.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(password)
            web.find_element(By.XPATH, '/html/body/div/div/div[2]/div/form/div[4]/button').click()
            web.switch_to.default_content()

            while 1:
                try:

                    #WebDriverWait(web,5,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="nc_1__scale_text"]')))

                    web.switch_to.frame('alibaba-login-box')
                    web.switch_to.frame('baxia-dialog-content')
                    span = web.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
                    action = ActionChains(web)
                    action.click_and_hold(span).perform()
                    action.move_by_offset(250,0).perform()
                    for i in range(3):
                        action.move_by_offset(5,0).perform()
                        time.sleep(0.1)
                    time.sleep(0.2)
                    action.release().perform()
                    web.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
                except StaleElementReferenceException:
                    web.refresh()









def main():
    user = '13295151779'
    password = 'chenhao#include0'
    login(user,password)





if __name__ == '__main__':

    #去除浏览器识别,规避服务器 显示正在受自动化程序控制
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('detach',True)
    opt.add_argument(     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    opt.add_argument('--disable-blink-feature=AutomationControlled')
    web = Chrome(options=opt)
    # 解决特征识别，避免浏览器识别非人为登录
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    web.execute_script(script)
    main()



































