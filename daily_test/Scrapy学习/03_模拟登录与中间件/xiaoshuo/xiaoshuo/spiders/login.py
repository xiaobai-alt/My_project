import scrapy


class LoginSpider(scrapy.Spider):  # 若是子类对父类提供的某个方法不满意，就可以采取重写函数
    name = "login"
    allowed_domains = ["17k.com"]
    start_urls = ["https://user.17k.com/www/bookshelf/read.html"]

    """
    此处重新定义对start_urls的处理
    重写init.py的start_requests()方法就可
    """

    def start_requests(self):
        # 方案一：直接网站登录后复制cookie值
        # cookies = """
        # GUID=239b1395-ccf3-4bf6-8045-3920d9eb6862; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100064599%22%2C%22%24device_id%22%3A%22187759ea16c3c2-052ea276590fdd8-d545429-1327104-187759ea16d809%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80…29ea10f4046c68a; Hm_lpvt_9793f42b498361373512340937deb2a0=1684940150; c_channel=0; c_csc=web; __root_domain_v=.17k.com; _qddaz=QD.986784939937945; BAIDU_SSP_lcr=https://www.baidu.com/link?url=-mLDhPLDH418bRcQbUAdE7a8Yyo2oEjfF4aGvsisLKC&wd=&eqid=803f46670010dd1c00000004646e250b; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F19%252F99%252F45%252F100064599.jpg-88x88%253Fv%253D1678264526000%26id%3D100064599%26nickname%3Dshenmndanfn%26e%3D1700492071%26s%3D4471ebda67ea5638
        # """
        # cookies_list = cookies.split('; ')
        # dic = {}
        # for it in cookies_list:
        #     k, v = it.split('=')
        #     dic[k.strip()] = v.strip()
        # yield scrapy.Request(
        #     url=self.start_urls[0],
        #     cookies=dic
        # )

        # 方案二：走登录流程
        # 发送post请求的第一个方案（不好用）
        url = 'https://passport.17k.com/ck/user/login'
        user = '13295151779'
        passwd = 'chenhao#include0'
        # yield scrapy.Request(
        #     url=url,
        #     method='post',
        #     body=f"loginName={user}&password={passwd}",
        #     # 与常规的post请求传参不同，不能采用字典，而是要将参数拼接起来
        #     # 例如此处，可以在谷歌开发者payload中查看form-data时点击view source查看编码后的参数信息
        #     callback=self.parse
        # )
        # 更常用的发送post的方案，默认post发送
        yield scrapy.FormRequest(
            url=url,
            formdata={
                'loginname':user,
                'password':passwd
            },
            callback=self.parse
        )
    def parse(self, response):
        yield scrapy.Request(url=LoginSpider.start_urls[0], callback=self.parse_detail)

    def parse_detail(self, resp):
        print(resp.text)
