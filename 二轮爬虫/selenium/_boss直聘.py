
#当网站验证过多时，可以考虑selenium爬取，可以考虑登录爬取，有风险
#不登录也可以，放缓爬取的速度

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

web = Chrome()

web.get('https://www.zhipin.com/web/user/?ka=header-login')

web.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div/div[2]/div[1]/div[1]/div/span[2]/input').send_keys('13295151779')















































