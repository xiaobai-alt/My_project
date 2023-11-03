import re

string = '车辆ID为:ticket_5j000G758890_18_19|出发地:常州  目的地:丹阳  出发时间:21:10  到达时间:21:26  Null一等座:G7588次列车，一等座票价34.5元，余票有  二等:G7588次列车，二等座票价19.5元，余票有  NullNull'

obj = re.compile(r'车辆ID为:(?P<id>.*?)出发地')
result = obj.finditer(string)
for i in result:
    x= i.group('id')
    print(x.strip('|'))