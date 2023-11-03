from selenium.common import ElementNotInteractableException, ElementNotVisibleException
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
import os
import time



# def chrome_create():
#     opt = Options()
#     opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
#     opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
#     web = Chrome(options=opt)
#     web.get('https://kyfw.12306.cn/otn/resources/login.html')
#     # 解除浏览器特征识别selenium
#     script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
#     web.execute_script(script)


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
    WebDriverWait(web, 5, 1).until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
    span = web.find_element(By.ID, 'nc_1_n1z')
    action = ActionChains(web)
    action.click_and_hold(span).move_by_offset(300,
                                               0).perform()  # click_and_hold代表点击并保持点击动作。move_by_offset(x, y)，其中x代表水平移动距离，y代表垂直移动距离
    time.sleep(1)
    web.refresh()
    WebDriverWait(web, 10, 1).until(EC.url_to_be('https://kyfw.12306.cn/otn/view/index.html'))
    pickle.dump(web.get_cookies(), open('./12306cookies.pkl', 'wb'))
    print('cookies保存成功')


def cookies_login():
    cookies = pickle.load(open('./12306cookies.pkl', 'rb'))
    for cookie in cookies:
        cookie_dic = {
            'domain': '.12306.cn',
            'name': cookie.get('name'),
            'value': cookie.get('value')
        }
        web.add_cookie(cookie_dic)
    web.get('https://kyfw.12306.cn/otn/leftTicket/init')
    print('cookies载入成功')


def get_ticket_info(start_city, end_city, date):
    WebDriverWait(web, 2, 0.5).until(EC.url_to_be('https://kyfw.12306.cn/otn/leftTicket/init'))

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
                tr_ying_wo = '硬卧:' + tr.xpath('./td[8]/@aria-label')[0] + ' '  # 硬卧
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


def chick_ticket(dic, id, count):
    # print('*' * 15 + '查询到的车次信息如下' + '*' * 30)
    # print(str(dic).replace(',', '\n'))
    # train_id = '车次:' + str(input('请输入选择的车次:\n'))  # 车次:与输入的车次num拼接为字典的key值
    train_id = '车次:' + id
    print('您选择的车次为：', id)
    while train_id in dic.keys():
        tr_info = dic.get(train_id)  # 根据key值信息获取到其保存在value里的id与座位信息等
        obj = re.compile(r'车辆ID为:(?P<id>.*?)出发地')  # 利用正则获取到车次id
        result = obj.finditer(tr_info)  # 此时获取到的是迭代器，要重新获取出来
        for i in result:
            tr_id = i.group('id').strip('|')  # 由于获取到的id中带有分隔符|，因此剔除掉
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新，实时获取本地时间
        if time_now == '17:33:05':  # 设定抢票时间，一般为下午五点：17:00:00
            web.refresh()
            web.find_element(By.ID, 'query_ticket').click()  # 点击重新查询
            WebDriverWait(web, 2, 0.1).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{tr_id}"]/td[13]/a')))
            web.find_element(By.XPATH, f'//*[@id="{tr_id}"]/td[13]/a').click()  # 根据id匹配到车次所在列并点击末尾的预定按钮
            WebDriverWait(web, 2, 0.1).until(EC.url_to_be('https://kyfw.12306.cn/otn/confirmPassenger/initDc'))
            if count == 1:
                my_self = 'N'  # 根据个人情况，如果有学生票选项的话就自己添加一个判断，我这里默认平时学生票为N，不选择
                web.find_element(By.ID, 'normalPassenger_0').click()
                WebDriverWait(web, 2, 0.1).until(EC.presence_of_element_located((By.ID, 'dialog_xsertcj_cancel')))
                if my_self == 'N':
                    web.find_element(By.ID, 'dialog_xsertcj_cancel').click()
                else:
                    web.find_element(By.ID, 'dialog_xsertcj_ok').click()
                web.find_element(By.ID, 'submitOrder_id').click()
                WebDriverWait(web, 100, 0.5).until(EC.element_to_be_clickable((By.ID, 'qr_submit_id')))
                # 注意这里的细节，由于Seenium自身的Bug，可能会导致确认点击操作无法正确执行
                submit_button = web.find_element(By.ID, 'qr_submit_id')
                try:
                    while submit_button:
                        try:
                            submit_button.click()
                            submit_button = web.find_element(By.ID, 'qr_submit_id')
                        except(ElementNotVisibleException, ElementNotInteractableException):
                            # 当在此页面见不到此元素，代表已进入付款页面
                            break
                    print('抢票成功，请尽快付款！')
                except:
                    pass


if __name__ == '__main__':
    #chrome_create()
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 去除浏览器顶部显示受自动化程序控制
    opt.add_experimental_option('detach', True)  # 规避程序运行完自动退出浏览器
    web = Chrome(options=opt)
    web.get('https://kyfw.12306.cn/otn/resources/login.html')
    # 解除浏览器特征识别selenium
    script = 'Object.defineProperty(navigator,"webdriver", {get: () => false,});'
    web.execute_script(script)
    user = ''  # 此处输入账号
    pwd = ''  # 此处输入密码
    start_city = '常州'
    end_city = '丹阳'
    date = '2023-05-23'  # 格式参照2023-05-17
    t_id = 'G7314'  # 想要选择的车次id
    person1 = ''  # 这里根据自己账号具体保存的个人信息选择乘车人，一人就只需定义一个person，多人数以此累加
    # person2 = ''
    person_list = []
    person_list.append(person1)  # person_list.append(person1，person2,person3, ......)
    person_count = len(person_list)

    if not os.path.exists('./12306cookies.pkl'):
        login(user, pwd)
        print('信息输入成功，请重新运行程序')
        web.close()
    else:
        stat_info = os.stat('./12306cookies.pkl')
        last_modify_time = time.time() - stat_info.st_mtime
        # print(last_modify_time)
        if last_modify_time > 1800:  # 建议半小时刷新一次cookie
            login(user, pwd)
            web.refresh()
            print('信息输入成功，请重新运行程序')
            web.close()
        else:
            cookies_login()  # 利用cookie实现快速登陆
            get_ticket_info(start_city, end_city, date)  # 获取到查询信息
            tick_dic = get_ticket_dic_info()  # 查询信息封装成字典传递给选票
            chick_ticket(tick_dic, t_id, person_count)   # 进行购票
