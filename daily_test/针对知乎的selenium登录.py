import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tujian import TuJian
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def login(user, password):
    web.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div['
                               '1]/div[2]').click()
    web.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div['
                               '2]/div/label/input').send_keys(user)
    time.sleep(0.2)
    web.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div['
                               '3]/div/label/input').send_keys(password)
    web.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button').click()

    #WebDriverWait(web,5,0.1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div['
                                                                             #'2]/div/div[1]/div/div[1]/img[1]')))
    time.sleep(1)
    png = web.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]').screenshot_as_base64

    result = int(TuJian.base64_api(uname='chen0525', pwd='chen123', img=png, typeid=33))
    # print('距离为', result)


    span = web.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]/span')
    while True:
        action = ActionChains(web)
        action.click_and_hold(span)
        for i in range(10):
            action.move_by_offset(result/10, 0)
            time.sleep(0.01)
            action.perform()
        action.release().perform()

        if web.title == '知乎 - 有问题，就会有答案':
            try:
                web.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button').click()
            except:
                break
        else:
            print('success')
            break




if __name__ == '__main__':

    # 去除浏览器显示受到自动化程序控制
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('detach', True)

    web = Chrome(options=opt)

    web.get('https://www.zhihu.com/signin?next=%2F')

    user = '13295151779'
    password = 'chenhao#include0'

    login(user, password)

























