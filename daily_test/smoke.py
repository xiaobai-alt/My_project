# -*- coding: utf-8 -*-
import random
import requests
import bs4
import os
import time
import json
import re
import pickle
import logging
import logging.handlers
import traceback

CURPATH=os.path.dirname(os.path.abspath(__file__))
LOG_FILENAME = CURPATH+'/smoking.log'

logger = logging.getLogger()


class SmokeWrapper(object):
    stockproducts = {}

    def __init__(self):
        self.sess = requests.Session()
        self.email = "nightcat@gmail.com"
        self.password = ""
        self.TOKEN = "5095276767:AAHVQj-QWhxLSQTAnb6fYs17B-ZywZKt3KU"  # 填tgtoken
        self.chat_id = "-904107496"  # 填tg chat_id
        # self.TOKEN = "6069924214:AAGCc-OV03b40P-pUGGFifnGvywlDEmd4FM"  # 填tgtoken,nc token
        # self.chat_id = "484362806"  # 填tg chat_id
        self.cookies = {
            # 'CFID': 'Z1zsqg2ooadbrddjnurc3ii4hsfr1k5v3uprjceh1slmh8mdskl-81681414',
            # 'CFTOKEN': 'Z1zsqg2ooadbrddjnurc3ii4hsfr1k5v3uprjceh1slmh8mdskl-42408705',
            '_gid': 'GA1.2.1016896406.1684625170',
            'RECENTLYVIEWED': '2018%2C2823%2C1994',
            'CFGLOBALS': 'urltoken%3DCFID%23%3D81681414%26CFTOKEN%23%3D42408705%23lastvisit%3D%7Bts%20%272023%2D05%2D20%2020%3A42%3A24%27%7D%23hitcount%3D48%23timecreated%3D%7Bts%20%272023%2D05%2D20%2019%3A26%3A08%27%7D%23cftoken%3D42408705%23cfid%3D81681414%23',
            '_ga': 'GA1.1.592197522.1684625170',
            '_ga_YSQFTYHYTP': 'GS1.1.1684628405.2.1.1684629774.0.0.0',
        }

        self.cookiefile = "data.pkl"

        self.headers = {
            'authority': 'www.smokingpipes.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            # 'cookie': 'CFID=Z1zsqg2ooadbrddjnurc3ii4hsfr1k5v3uprjceh1slmh8mdskl-81681414; CFTOKEN=Z1zsqg2ooadbrddjnurc3ii4hsfr1k5v3uprjceh1slmh8mdskl-42408705; _gid=GA1.2.1016896406.1684625170; RECENTLYVIEWED=2018%2C2823%2C1994; CFGLOBALS=urltoken%3DCFID%23%3D81681414%26CFTOKEN%23%3D42408705%23lastvisit%3D%7Bts%20%272023%2D05%2D20%2020%3A42%3A24%27%7D%23hitcount%3D48%23timecreated%3D%7Bts%20%272023%2D05%2D20%2019%3A26%3A08%27%7D%23cftoken%3D42408705%23cfid%3D81681414%23; _ga=GA1.1.592197522.1684625170; _ga_YSQFTYHYTP=GS1.1.1684628405.2.1.1684629774.0.0.0',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }
        self.sess.headers.update(self.headers)
        if os.path.exists(self.cookiefile):
            self.restore_session_cookie(self.cookiefile)
        else:
            self.sess.cookies.update(self.cookies)

    def run(self):
        while True:
            self.runtask()
            logger.info("-------waiting for next turn--------\n")
            time.sleep(120)  # 延迟两分钟下一轮。

    def runtask(self):
        with open(CURPATH+"/tp.txt", "r+") as f:
            for url in [x.strip() for x in f.readlines() if not x.startswith("#")]:
                try:
                    if "product_id" in url:
                        info = self.checkproduct(url)
                        if info:
                            self.notifyproduct(info)
                    else:
                        for info in [i for i in self.checkcategory(url) if i]:
                            self.notifyproduct(info)
                except Exception as e:
                    logger.info("request:"+url+"\t"+str(e))
                    logging.info(traceback.print_exc())

                time.sleep(random.randint(10, 20) / 10)  # 每个页面延迟1~2秒

    def checkcategory(self, url):
        rs = self.sess.get(url)
        if rs.status_code != 200:
            logger.info(f"fetch {url} error code:{rs.status_code}")
            return
        # with open("category","w") as f:
        #     f.write(rs.text)
        # with open("category","r+") as f:
        #     text=f.read()
        soup = bs4.BeautifulSoup(rs.text, "html.parser")
        tags = soup.select('div.product')
        for tag in tags:
            # print(tag)
            product_id = tag['data-productid']
            href = tag.select_one('h3 > a:nth-child(3)')
            product_name = href.text
            price_tag = tag.select_one('.price > span:nth-child(1)')
            price = price_tag.text
            if "Stock" not in price:
                yield {"product_id": product_id, "product_name": product_name, "price": price, "stock": True}
            else:
                yield {"product_id": product_id, "product_name": product_name, "price": None, "stock": False}

    def checkproduct(self, url):
        product_id = re.search(r"/product_id/(\d+)", url).group(1)
        rs = self.sess.get(url)
        if rs.status_code != 200:
            logger.info(f"fetch {url} error code:{rs.status_code}")
            return
        # with open("product.txt","w") as f:
        #     f.write(rs.text)
        # with open("product.txt","r+") as f:
        #     text=f.read()
        soup = bs4.BeautifulSoup(rs.text, "html.parser")
        product_name = soup.select_one('div.detailPage-catProdNameWrap > h1').text.strip("\n\r ").split("\n")[0]
        idtag = soup.select_one('input[name=Product_id]')
        if idtag is None:
            # logger.info(f"Out of stock,name: {product_name}  id: {product_id}")
            return {"product_id": product_id, "product_name": product_name, "price": None, "stock": False}
        fetch_product_id = idtag['value']
        if fetch_product_id != product_id:
            logger.error(f"fetch {url} product_id error,origin:{product_id}  new product id:{fetch_product_id}")
        price = soup.select_one('.detailPage-yourPrice').text.strip().split(" ")[0]
        return {"product_id": product_id, "product_name": product_name, "price": price, "stock": True}

    # 通知到telegram，或是跳过不处理
    def notifyproduct(self, product_info):
        product_id, product_name, price, stock = product_info.values()
        if not stock:  # out of stock
            if self.stockproducts.get(product_id):
                del (self.stockproducts[product_id])
            return
        count = self.stockproducts.get(product_id)
        if count is None:
            self.stockproducts[product_id] = 1  # 首次初始化
        elif count >= 3:  # 检查到3次，直接返回不处理。
            return
        else:
            self.stockproducts[product_id] = self.stockproducts[product_id] + 1  # 计数+1

        logger.info(
            f"{product_name}\nprice:{price}\n https://www.smokingpipes.com/moreinfo.cfm?product_id={product_id}")
        self.sendmessage(
            f"{product_name}\nprice:{price}\n https://www.smokingpipes.com/moreinfo.cfm?product_id={product_id}")

        # logger.info(
        #     f"{product_name}\nprice:{price}\n https://www.smokingpipes.com/moreinfo.cfm?product_id={product_id}")
        # self.sendmessage(
        #     f"{product_name}\nprice:{price}\n https://www.smokingpipes.com/moreinfo.cfm?product_id={product_id}")
        pass

    def login(self):
        params = {
            'action': 'login',
            'from': '',
        }

        data = {
            'email': self.email,
            'password': self.password,
        }

        response = self.sess.post(
            'https://www.smokingpipes.com/checkout/login.cfm',
            params=params,
            data=data
        )
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            alert_tag = soup.select_one('div.alert')
            if alert_tag is None:
                print('Successfully logged in.')
                return True
            else:
                print("Login error " + alert_tag.text.strip())
                return False
        else:
            print('Login failed. HTTP request error')
            return False

    def save_session_cookie(self, filename):
        # Serialize the session cookies with the Pickle module.
        with open(filename, 'wb') as f:
            pickle.dump(self.sess.cookies, f)

    def restore_session_cookie(self, filename):
        # Deserialize the session cookies from the file.
        with open(filename, 'rb') as f:
            cookies = pickle.load(f)

        # Set the session cookies to the deserialized cookies.
        self.sess.cookies.update(cookies)

    # check for login
    def is_login(self):
        response = self.sess.head("https://www.smokingpipes.com/checkout/index.cfm")
        if response.status_code == 302 and response.headers['location'] != "/checkout/login.cfm":
            # "checkout-addresses.cfm" logined
            # if /checkout/login.cfm will need login first
            return True
        else:
            return False

    def sendmessage(self, desp):
        "https://www.smokingpipes.com/moreinfo.cfm?product_id=2018"
        data = (('chat_id', self.chat_id), ('text', '🐉监控脚本为您播报🐉 \n\n' + desp))
        response = requests.post('https://api.telegram.org/bot' + self.TOKEN +
                                 '/sendMessage',
                                 data=data)
        if response.status_code != 200:
            logger.info('Telegram Bot 推送失败')
        else:
            logger.info('Telegram Bot 推送成功')
        response = requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token=7b484e7d1370353a786b524eb5d21204fdbca3b9577c3f827ede569ce30e7f8f",
            json={"msgtype": "text", "text": {"content": '[草来] - 🐢监控脚本为您播报🐢 \n\n' + desp}})
        if response.status_code != 200:
            logger.info('Dingding 推送失败')
        else:
            logger.info('Dingding 推送成功')


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()

if __name__ == '__main__':
    sw = SmokeWrapper()
    sw.run()

