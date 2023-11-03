import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from lxml import etree
import re
import pickle


# 定义登录方法
def login(user, pwd):
    login_choice = web.find_element(By.XPATH, '//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[1]')
    # 点击账号密码登录方式
    login_choice.click()
    username = web.find_element(By.XPATH, '//*[@id="J-userName"]')  # 向账号框传入账号信息
    passwd = web.find_element(By.XPATH, '//*[@id="J-password"]')  # 向密码框传入密码
    username.click()
    username.send_keys(user)
    passwd.click()
    passwd.send_keys(pwd)
    # 定位到登录按钮并点击
    web.find_element(By.XPATH, '//*[@id="J-login"]').click()
    # 设置显示等待直到滑块的span标签被定位到
    WebDriverWait(web, 2, 0.5).until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
    span = web.find_element(By.ID, 'nc_1_n1z')
    action = ActionChains(web)
    action.click_and_hold(span).move_by_offset(300, 0).perform() # click_and_hold代表点击并保持点击动作。move_by_offset(x, y)，其中x代表水平移动距离，y代表垂直移动距离


def get_ticket_info(start_city, end_city, date):
    WebDriverWait(web, 2, 0.5).until(EC.presence_of_element_located((By.ID, 'link_for_ticket')))
    web.find_element(By.ID, 'link_for_ticket').click()

    web.find_element(By.ID, 'fromStationText').click()  # 先定位到出发地输入框点击后再传入参数
    web.find_element(By.ID, 'fromStationText').send_keys(start_city, Keys.ENTER)  # Keys库可以模拟实现键盘上的功能键

    web.find_element(By.ID, 'toStationText').click()  # 目的地
    web.find_element(By.ID, 'toStationText').send_keys(end_city, Keys.ENTER)

    web.find_element(By.ID, 'train_date').clear()  # 由于date页面默认当天日期，所以先清空默认内容在输入参数
    web.find_element(By.ID, 'train_date').send_keys(date, Keys.ENTER)

    web.find_element(By.ID, 'query_ticket').click()  # 点击查询


def get_ticket_dic_info():
    WebDriverWait(web, 2, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="queryLeftTable"]/tr')))
    tree = etree.HTML(web.page_source)
    tick_list = tree.xpath('//*[@id="queryLeftTable"]/tr')
    tr_dic = {}
    for tr in tick_list:
        if not tr.xpath('./td[1]/div/div[1]/div/a/text()'):
            continue
        else:
            tr_num = '车次:' + tr.xpath('./td[1]/div/div[1]/div/a/text()')[0]
            tr_id = '车辆ID为:' + tr.xpath('./@id')[0] + '|'  # 添加标识头和分隔符便于观看
            tr_from_place = '出发地:' + tr.xpath('./td[1]/div/div[2]/strong[1]/text()')[0] + '  '
            tr_get_place = '目的地:' + tr.xpath('./td[1]/div/div[2]/strong[2]/text()')[0] + '  '
            tr_start_time = '出发时间:' + tr.xpath('./td[1]/div/div[3]/strong[1]/text()')[0] + '  '  # 列车发动时间
            tr_get_time = '到达时间:' + tr.xpath('./td[1]/div/div[3]/strong[2]/text()')[0] + '  '  # 列车到达目的地时间
            if not tr.xpath('./td[2]/@aria-label'):
                tr_shang_wu = 'Null'
            else:
                tr_shang_wu = '商务座:' + tr.xpath('./td[2]/@aria-label')[0] + '  '  # 商务座
            if not tr.xpath('./td[3]/@aria-label'):
                tr_yi_deng = 'Null'
            else:
                tr_yi_deng = '一等座:' + tr.xpath('./td[3]/@aria-label')[0] + '  '  # 一等座
            if not tr.xpath('./td[4]/@aria-label'):
                tr_er_deng = 'Null'
            else:
                tr_er_deng = '二等:' + tr.xpath('./td[4]/@aria-label')[0] + '  '  # 二等座
            if not tr.xpath('./td[6]/@aria-label'):
                tr_ruan_wo = 'Null'
            else:
                tr_ruan_wo = '软卧:' + tr.xpath('./td[6]/@aria-label')[0] + '  '  # 软卧
            if not tr.xpath('./td[8]/@aria-label'):
                tr_ying_wo = 'Null'
            else:
                tr_ying_wo = '硬卧:' + tr.xpath('./td[8]/@aria-label')[0] + ' '   # 硬卧
            if not tr.xpath('./td[10]/@aria-label'):
                tr_ying_zuo = 'Null'
            else:
                tr_ying_zuo = '硬座:' + tr.xpath('./td[10]/@aria-label')[0] + ' '  # 硬座
            if not tr.xpath('./td[11]/@aria-label'):
                tr_wu_zuo = 'Null'
            else:
                tr_wu_zuo = '无座:' + tr.xpath('./td[11]/@aria-label')[0]  # 无座
            tr_dic[tr_num] = tr_id + tr_from_place + tr_get_place + tr_start_time + tr_get_time + tr_shang_wu + \
                            tr_yi_deng + tr_er_deng + tr_ruan_wo + tr_ying_wo + tr_ying_zuo + tr_wu_zuo
    return tr_dic


def chick_ticket(dic):
    print('*'*15+'查询到的车次信息如下'+'*'*30)
    print(str(dic).replace(',', '\n'))
    train_id = '车次:' + str(input('请输入选择的车次:\n'))  # 车次:与输入的车次num拼接为字典的key值
    if train_id in dic.keys():
        tr_info = dic.get(train_id)  # 根据key值信息获取到其保存在value里的id与座位信息等
    obj = re.compile(r'车辆ID为:(?P<id>.*?)出发地')  # 利用正则获取到车次id
    result = obj.finditer(tr_info)  # 此时获取到的是迭代器，要重新获取出来
    for i in result:
        tr_id = i.group('id').strip('|')  # 由于获取到的id中带有分隔符|，因此剔除掉
    web.find_element(By.XPATH, f'//*[@id="{tr_id}"]/td[13]/a').click()  # 根据id匹配到车次所在列并点击末尾的预定按钮


if __name__ == '__main__':
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
    opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
    web = Chrome(options=opt)
    web.get('https://kyfw.12306.cn/otn/resources/login.html')
    # 解除浏览器特征识别selenium
    script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
    web.execute_script(script)
    user = ''  # 此处输入账号
    pwd = ''   # 此处输入密码
    start_city = ''
    end_city = ''
    date = ''

    login(user, pwd)

    get_ticket_info(start_city, end_city, date)
    tick_dic = get_ticket_dic_info()
    chick_ticket(tick_dic)














































