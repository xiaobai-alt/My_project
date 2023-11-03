from openpyxl import Workbook

wb = Workbook()

# 获取当前工作表
sheet = wb.active
print(sheet.title)

sheet.title = '测试'

# 创建一个新的xlsx文件
wb.save('test.xlsx')