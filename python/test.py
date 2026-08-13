# num = 22.236
# print('%.2f' % num)
# from decimal import Decimal
# Decimal('22.345')
# Decimal(str(num)).quantize(Decimal('0.00'),rounding="ROUND_HALF_UP")

# h = float(input('请输入身高'))
# w = float(input('请输入体重'))

# BMI = w / h ** 2
# print('%.2f' % BMI)
f = open('test.txt',encoding='gbk')
print(f.read(10))