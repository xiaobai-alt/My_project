import json
from lxml import etree
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

# url = 'https://www.tobaccopipes.com/lane-limited-1-q-pipe-tobacco/'
# url = 'https://www.tobaccopipes.com/cornell-diehl-small-batch-sun-bear-tupelo-pipe-tobacco/'
url_list = ['https://www.tobaccopipes.com/lane-limited-1-q-pipe-tobacco/', 'https://www.tobaccopipes.com/cornell-diehl-small-batch-sun-bear-tupelo-pipe-tobacco/']
for url in url_list:
    resp = requests.get(url).text
    tree = etree.HTML(resp)
    exist = tree.xpath('//input[@id="form-action-addToCart"]')
    if not exist:
        print('false')
    else:
        print(url)
        print(exist)
# print(resp)


# 有货状态会显示为id为form-action-addToCart的input标签
# 无货状态通常会有id为InStockNotifyClick的input标签








