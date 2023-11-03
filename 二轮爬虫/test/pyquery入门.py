from pyquery import PyQuery

html = """
<ul>
    <li class="aaa"><a href="https://www.baidu.com">百度</a></li>
    <li class="bbb"><a href="https://www.google.com">谷歌</a></li>
    <li class="aaa"><a href="https://www.souhu.com">搜狐</a></li>
    <li class="ccc" id="qq"><a href="https://www.qq.com">qq</a></li>
    
</ul>
"""



#加载html内容
p = PyQuery(html)

#在标签后面添加新标签
p("li.ccc").after("""<li class="ddd"><a>新插入</a></li>""")
#在标签内部添加内容
p("li.ddd").append("""<span>添加内容</span>""")
#添加属性
p("li.ddd").attr('id','123456')  #p().remove_attr()删除属性    p("").remove 删除标签
print(p)





# a = p(".aaa a")  #.class
# # print(type(p))
# print(a)
# b = p("#qq a").attr("href")  #  ("#idName 标签").attr("属性")
# b1 = p("#qq a").text()  #直接获取文本
# print(b,'\n',b1)
#pyquery对象直接(css选择器)
#
# li = p("li")
# a = p("a")  #此时获取的li,a依旧是pyquery对象，可以继续进行提取
# print(li,'\n',a)
#
# a1 = li("a")
# print(a1)

#a = p("li a") #后代选择，直接获取li下的a

#批量获取多个标签属性值时，默认返回获取的第一个
#如何获取全部
# it= p("li a").items() #获取属性值的迭代器
# for i in it:
#     href = i.attr("href")
#     text = i.text()
#     print(href,text)


# div = """
# <div><span>测试</span></div>
# """
# q = PyQuery(div)
#
# html = q("div").html() #html获取的是所选择的选择器里所有内容，包括html代码
# test = q("div").text()
# print(html,test)























