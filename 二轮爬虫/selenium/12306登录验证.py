import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys #模拟键盘按键的包
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def login(user,password):
    web.implicitly_wait(10)

    web.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/ul/li[1]/a').click()

    web.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(user)

    web.find_element(By.XPATH, '//*[@id="J-password"]').send_keys(password)

    web.find_element(By.XPATH, '//*[@id="J-login"]').click()

    span = web.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/span')

    action = ActionChains(web)

    action.click_and_hold(span).move_by_offset(300, 0).perform()

    action.release()

def get_ticket(start,where,date):
    # 点击车票预订选项
    web.find_element(By.XPATH, '//*[@id="link_for_ticket"]').click()

    time.sleep(1)

    web.find_element(By.XPATH, '//*[@id="fromStationText"]').click()
    web.find_element(By.XPATH, '//*[@id="fromStationText"]').send_keys(start, Keys.ENTER)

    web.find_element(By.XPATH, '//*[@id="toStationText"]').click()
    web.find_element(By.XPATH, '//*[@id="toStationText"]').send_keys(where, Keys.ENTER)

    # 先清空日期
    web.find_element(By.XPATH, '//*[@id="train_date"]').clear()
    web.find_element(By.XPATH, '//*[@id="train_date"]').send_keys(date, Keys.ENTER)

    time.sleep(0.1)
    # 点击查询按钮
    web.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
    #WebDriverWait(web,10,0.5).until(EC.url_to_be('https://kyfw.12306.cn/otn/leftTicket/init'))
    WebDriverWait(web, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="queryLeftTable"]/tr')))
    page = web.page_source
    tree = etree.HTML(page)
    info_list = tree.xpath('//*[@id="queryLeftTable"]/tr')
    # web.find_element(By.XPATH,'//*[@id="queryLeftTable"]')
    if not info_list:
        print('*' * 30)
        print(f'Sorry,未查询到{date}从{start}到{where}的列车')
        exit(1)
    tr_dic = {}

    for tr in info_list:
        if not tr.xpath('./td[1]/div/div[1]/div/a/text()'):
            continue
        else:
            tr_num = '车次:' + tr.xpath('./td[1]/div/div[1]/div/a/text()')[0]
        tr_id = '车辆ID为:' + tr.xpath('./@id')[0] + '|'
        tr_strplace = '出发地:' + tr.xpath('./td[1]/div/div[2]/strong[1]/text()')[0] + '  '
        tr_getplace = '目的地:' + tr.xpath('./td[1]/div/div[2]/strong[2]/text()')[0] + '  '
        tr_Stime = '出发时间:' + tr.xpath('./td[1]/div/div[3]/strong[1]/text()')[0]  + '  '  # 列车发动时间
        tr_gettime ='到达时间:' +  tr.xpath('./td[1]/div/div[3]/strong[2]/text()')[0] + '  '  #列车到达目的地时间
        if not tr.xpath('./td[2]/@aria-label'):
            tr_shangwu = 'Null'
        else:
            tr_shangwu = '商务座:' + tr.xpath('./td[2]/@aria-label')[0] + '  '  # 商务座
        if not tr.xpath('./td[3]/@aria-label'):
            tr_yideng = 'Null'
        else:
            tr_yideng = '一等座:' + tr.xpath('./td[3]/@aria-label')[0]+ '  ' #一等座
        if not tr.xpath('./td[4]/@aria-label'):
            tr_erdeng = 'Null'
        else:
            tr_erdeng = '二等:' + tr.xpath('./td[4]/@aria-label')[0] + '  ' # 二等座
        if not tr.xpath('./td[6]/@aria-label'):
            tr_ruanwo = 'Null'
        else:
            tr_ruanwo ='软卧:' +  tr.xpath('./td[6]/@aria-label')[0] + '  ' # 软卧
        if not tr.xpath('./td[8]/@aria-label'):
            tr_yingwo ='Null'
        else:
            tr_yingwo = '硬卧:' + tr.xpath('./td[8]/@aria-label')[0]  #硬卧
        tr_dic[tr_num] = tr_id+tr_strplace+tr_getplace+tr_Stime+tr_gettime+tr_shangwu+tr_yideng+tr_erdeng+tr_ruanwo+tr_yingwo
    return tr_dic


def choice_ticket(dic):
    print('查询到的列车信息如下:\n')
    print(str(dic).replace(',', '\n'))
    tick_pid = '车次:' + str(input('请按标准输入想要购买的车次编号:\n'))

    if tick_pid in dic.keys():
        pid = dic.get(tick_pid)
        # pid = tic_list.index(tick_pid) + 1
    obj = re.compile(r'车辆ID为:(?P<id>.*?)出发地')
    result = obj.finditer(pid)
    for i in result:
        x = i.group('id').strip('|')

    time.sleep(1)
    web.find_element(By.XPATH, f'//*[@id="{x}"]/td[13]/a').click()
    # #order_btn = web.find_element(By.XPATH,f'//*[@id="queryLeftTable"]/tr[{pid}]/td[13]/a').click()
    # #//*[@id="ticket_55000D166802_03_04"]/td[13]/a

    WebDriverWait(web, 10,0.5).until(EC.url_to_be('https://kyfw.12306.cn/otn/confirmPassenger/initDc'))
    # #
    people = int(input('请输入购票人数:\n'))
    student = str(input('请确定是否为学生票，y/n:'))

    if people == 1:
        web.find_element(By.XPATH, '//*[@id="normalPassenger_0"]').click()
        if student == 'y':
            web.find_element(By.XPATH,'//*[@id="dialog_xsertcj_ok"]').click()
            web.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()

            WebDriverWait(web, 10, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="content_checkticketinfo_id"]/div[1]')))
            web.find_element(By.XPATH,'//*[@id="content_checkticketinfo_id"]/div[1]').click()

            a = web.find_elements(By.XPATH, '//*[@id="erdeng1"]/ul[2]')
            if len(a) == 1:
                web.find_element(By.XPATH, '//*[@id="erdeng1"]/ul[2]/li[2]/a').click()
                web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
            else:
                web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
        else:
            web.find_element(By.XPATH,'//*[@id="dialog_xsertcj_cancel"]').click()
            web.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()

            WebDriverWait(web, 10, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]')))
            web.find_element(By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]').click()

            a = web.find_elements(By.XPATH,'//*[@id="erdeng1"]/ul[2]')
            if len(a) ==1:
                web.find_element(By.XPATH, '//*[@id="erdeng1"]/ul[2]/li[2]/a').click()
                web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
            else:
                web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
    elif people >= 2:
        for i in range(people+1):
            web.find_element(By.XPATH,f'//*[@id="normalPassenger_{i}"]').click()
            if student == 'y':
                web.find_element(By.XPATH, '//*[@id="dialog_xsertcj_ok"]').click()
                web.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()

                WebDriverWait(web, 10, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]')))
                web.find_element(By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]').click()

                a = web.find_elements(By.XPATH, '//*[@id="erdeng1"]/ul[2]')
                if len(a) == 1:
                    web.find_element(By.XPATH, '//*[@id="erdeng1"]/ul[2]/li[2]/a').click()
                    web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
                else:
                    web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
            else:
                web.find_element(By.XPATH, '//*[@id="dialog_xsertcj_cancel"]').click()
                web.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()

                WebDriverWait(web, 10, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]')))
                web.find_element(By.XPATH, '//*[@id="content_checkticketinfo_id"]/div[1]').click()

                a = web.find_elements(By.XPATH, '//*[@id="erdeng1"]/ul[2]')
                if len(a) == 1:
                    web.find_element(By.XPATH, '//*[@id="erdeng1"]/ul[2]/li[2]/a').click()
                    web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
                else:
                    web.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()


if __name__ == '__main__':
    #去除浏览器识别,规避服务器 显示正在受自动化程序控制
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('detach',True)

    web = Chrome(options=opt)
    web.get('https://kyfw.12306.cn/otn/resources/login.html')
    # 解决特征识别，避免浏览器识别非人为登录
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    web.execute_script(script)
    #print('请输入用户名与密码')
    user = ''#str(input('用户名：'))
    password = ''#str(input('密码：'))
    start = '常州'#str(input('请输入出发地：\n'))
    where = '丹阳'#str(input('请输入目的地：\n'))
    date = '2023-04-04'#str(input('请按照2023-03-29的格式输入日期：\n'))

    login(user,password)

    ticket_dic = get_ticket(start,where,date)

    choice_ticket(ticket_dic)











































































