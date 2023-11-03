
from selenium.webdriver import Chrome
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.chrome.options import Options

# 官网
damai_url = 'https://www.damai.cn/'

# 登录页面
login_url = 'https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F'

# 需要抢票的链接
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.591b23e1kHnWBo&id=709352773215'


class Concert:
    """初始化设置"""
    def __init__(self):
        self.status = 0  # 状态， 表示当前操作执行到了那个步骤
        self.login_method = 1  # {0：模拟登录， 1：cookies登录}
        opt = Options()
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        opt.add_experimental_option('detach', True)  # 运行完不关闭窗口
        script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
        self.driver = Chrome(options=opt)
        self.driver.execute_script(script)

    # cookies：用来记录登录信息的文件
    def set_cookies(self):
        self.driver.get(login_url)
        print('###请扫码登录###')
        self.driver.switch_to.frame('alibaba-login-box')
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div[3]')))
        self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[3]').click()
        WebDriverWait(self.driver, 10, 0.5).until(EC.url_to_be('https://www.damai.cn/'))
        print('###登录成功###')
        pickle.dump(self.driver.get_cookies(), open('cookies.pkl', 'wb'))
        print('###cookies保存成功###')
        self.driver.get(target_url)

    """获取当前已保存的cookies.pkl"""
    def get_cookies(self):
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            cookie_dict = {
                'domain': '.damai.cn',
                'name': cookie.get('name'),
                'value': cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)
        self.driver.get(target_url)
        print('###cookie载入成功###')

    """登录"""
    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
        elif self.login_method == 1:
            # 接着判断当前目录下是否有cookies文件
            if not os.path.exists('cookies.pkl'):
                # 切换到登录界面，登录信息记录
                self.set_cookies()
            else:

                self.driver.get(target_url)
                self.get_cookies()

    """打开浏览器动作"""
    def enter_concert(self):
        print('###打开浏览器，进入大麦网')
        self.login()
        self.driver.refresh()
        self.status = 2
        print('###登录成功###')

    """抢票并提交订单"""
    def choose_ticket(self):
        if self.status == 2:
            print('*'*30)
            print('场次确认')


if __name__ == '__main__':
    con = Concert()
    con.enter_concert()























