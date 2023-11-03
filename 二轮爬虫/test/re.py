#借助re模块在python中使用正则表达式
import re
#
# result = re.findall(r'\d+','我是一个abcda13212321')   #findall(r'x','y')  y为要被匹配的字符串,在x前面加上r来避免转义字符
# print(result)


# #最经常使用的
# result = re.finditer(r'\d+','我是一个abcda13212321,我有10000块')  #finditer返回的是一个迭代器
# for item in result:    #从迭代器中拿内容
#     print(item.group())  #从匹配的结果中获取数据



#相较于finditer,search只能匹配第一次匹配的数据
# result = re.search(r'\d+','我叫蔡徐坤，今年18岁，我有100000多亿粉丝')
# print(result)


#match,在匹配的时候是从字符串开头进行匹配
# result = re.match(r'\d+','我叫蔡徐坤，今年18岁，我有100000多亿粉丝')
# print(result)



#预加载，提前吧正则对象加载完毕.再循环中能有效改善运行

# obj = re.compile(r'\d+')
# result = obj.findall('我叫蔡徐坤，我有1000000000粉丝，都是小鸡子123')
# print(result)

#简单测试
s = """
<div class = '西游记'><span id='10086'>中国移动</span></div>
<div class = '西游记'><span id='10010'>中国联通</span></div>
"""
obj = re.compile(r"<span id='(\d+)'>(.*?)</span>")  #加上括号可直接获取想要匹配的值
result = obj.findall(s)
print(result)
# obj = re.compile(r"<span id='(?P<id>.*?)'>(?P<name>.*?)</span>") #若要规范化结果，使用迭代器
# result = obj.finditer(s)
# for item in result:
#     id = item.group('id')
#     print(id)
#     name = item.group('name')
#     print(name)































