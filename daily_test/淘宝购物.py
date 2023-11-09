import time
import os
import random
import pickle
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def create_driver():
    """创建driver并保存cookie"""
    os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="F:\selenium"')
    # 在此之前的任何操作不会影响到后续逻辑，建议手动完成登录操作
    input('输入空格继续程序...')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    driver = Chrome(options=options)
    pickle.dump(driver.get_cookies(), open('./taobao_cookies.pkl', 'wb'))
    print('cookies保存成功')


def cookies_login():
    web.get(
        'https://cart.taobao.com/cart.htm?spm=a21bo.jianhua.1997525049.1.5af92a89tv8ELa&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')
    cookies = pickle.load(open('./taobao_cookies.pkl', 'rb'))
    for cookie in cookies:
        cookie_dic = {
            'domain': '.taobao.com',
            'name': cookie.get('name'),
            'value': cookie.get('value')
        }
        web.add_cookie(cookie_dic)
    web.get(
        'https://cart.taobao.com/cart.htm?spm=a21bo.jianhua.1997525049.1.5af92a89tv8ELa&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')
    print('cookies载入成功')


if __name__ == '__main__':
    if not os.path.exists('./taobao_cookies.pkl'):
        create_driver()
        print('信息输入成功，请重新运行程序')
        # web.close()
    else:
        stat_info = os.stat('./taobao_cookies.pkl')
        last_modify_time = time.time() - stat_info.st_mtime
        # print(last_modify_time)
        if last_modify_time > 1800:  # 建议半小时刷新一次cookie
            create_driver()
            # web.refresh()
            # print('信息输入成功，请重新运行程序')
            # web.close()
        else:
            opt = Options()
            opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
            opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
            web = Chrome(options=opt)
            # 解除浏览器特征识别selenium
            script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
            web.execute_script(script)
            cookies_login()  # 利用cookie实现快速登陆
            # 此时以及进入购物车，可以设置定点点击购物
            # time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新，实时获取本地时间
            # if time_now == '': # 自己设置定时时间
            web.find_element(By.XPATH,
                             '/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[6]/div/div[1]/div/div/label').click()
            time.sleep(round(random.uniform(0.1, 2), 1))
            web.find_element(By.XPATH, '//*[@id="J_Go"]').click()
            WebDriverWait(web, 5, 0.5).until(EC.title_is('确认订单 - Tmall.com天猫-理想生活上天猫'))
            # 点击提交订单
            web.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div[9]/div/div/a[2]').click()
            # 后续付款可在页面或手机上完成
