## 一、数据类型
  ### 1.1 数值型
  - int整型
  - float浮点型
  - bool布尔型
  ### 1.2 容器，包括(有序容器)和(无序容器)
  - 字符串str(有序容器)
  - 列表list(有序容器)
  - 元组tuple(有序容器)
  - 字典dict(无序容器)
  - 集合set(无序容器)
  ### 1.3类
  ### 1.4 虚数、复数
  - complex
  ### 1.5 类型转换
  - int(x,[base]),转化为整数
  - float(x),转化为浮点数
  - complex(real,[imag]),创建一个复数，real为实部，imag为虚部
  - str(x),将对象x转化为字符串
  - repr(x),将对象x转化为表达式字符串
  - eval(x),用来计算在字符串中的有效python表达式，并返回一个对象
  - tuple(s),将序列s转化为一个元组
  - list(s),将序列s转化为一个列表
  ### 1.6 输出格式化
  - %
  - f'我的名字是{name}'
  ```py
  num = 22.234
  print('%.2f' % num)
  from decimal import Decimal
  Decimal('22.345')
  Decimal(str(num)).quantize(Decimal('0.00'),rounding="ROUND_HALF_UP")
  ```

## 二、运算符
- 算数运算符：+-*/,//整除,%取余,**指数(2**4=2的4次方),()
- 赋值运算符
- 复合赋值运算符
- 比较运算符
- 逻辑运算符
## 三、语句
- if
- while
- for
## 四、字符串操作
- 切片
- isalpha
- isspace
- isidentifier
- isdigit
- islower
- startswith
- endswith
- istrip(str)
- rstrip(str)去掉右边的str字符
- strip(str)去掉左右两边的srt字符
- find
- upper,lower,swapcase,capitalize,title
## 五、列表list