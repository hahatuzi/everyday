## 一、数据类型
  ### 1.1 数值型
  - **int**整型
  - **float**浮点型
  - **bool**布尔型
  ### 1.2 容器，包括(有序容器)和(无序容器)
  - 字符串**str**(有序容器)
  - 列表**list**(有序容器)
  - 元组**tuple**(有序容器)
  - 字典**dict**(无序容器)
  - 集合**set**(无序容器)
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
## 五、列表list操作
- 下标和切片
- index函数
- count函数
- len函数
- append函数
- extend函数
- insert
- pop
- del
- remove
- reverse
- sort
- for
## 六、元组及其操作
> 元组是由一系列变量组成的不可变序列容器，不可变是指创建完成后不能再添加，删除，修改元素。
- 下标和切片
- index函数
- count函数
- len函数
- for循环
## 七、python内置函数操作
- len(x)返回序列的长度
- max(x)返回序列的最大值元素
- min(x)返回序列的最小值元素
- sum(x)返回序列中所有元素的和，元素必须是数值类型
## 八、容器
- 序列：list,string,tuple
- 映射:字典dict
- 集合:set
## 九、字典操作
- 增删改：字典序列[key] = 值，del d[key]
- len(dict)
- d[k]
- k in d
- clear:清除字典中的所有数据
- fromkeys:创建一个新字典，包含指定的键，键值都是none
- get:直接访问字典中的值
- items：返回一个包含所有字典项的列表，每个元素都是键值对的形式
- keys:返回字典中的所有key,组成一个列表
- values:返回字典中所有的value
- pop:删除并返回指定key的值
## 十、函数
  ### 内置高阶函数
  - sorted(list)函数，可以对list进行排序
  - filter(函数， list),过滤
  - map(函数， list),过滤
  - reduce(函数， list),
  ```js
  def not_odd(num):
    return n % 2 == 0
  
  filter(not_odd, [1,2,3,4,5,6])
    sorted([36,5,-12,9,-21])
  ```
## 十一、文件和目录的操作
  ### 11.1 IO流Stream
  - read()
  - readlines()
  - readline()
  - write()
  - seek(偏移量,)
  - tell()
  ### 11.2 OS，访问操作系统功能
  - os.name
  - os.sep,获取当前系统平台路径分隔符
  - os.getcwd,获取当前工作目录
  - os.environ[key],获取当前环境变量值
  - os.listdir,列出指定目录path的所有文件和目录名
  - os.mkdir/makedirs,创建单层目录，多层目录
  - os.path.abspath
  - os.path.split
  - os.remove,删除文件
## 十二、对象
  ### 12.1 init函数
  > __init():对象的初始化函数,创建独享的时候默认被调用，无需手动调用
  > __init(self)
  ### 12.2 str函数
  > 当使用了print输出对象的时候，默认打印对象的内存地址。如果类定义了_str__方法，就会打印从这个函数return出去的数据
  ### 12.3 del函数
  > 当删除对象的时候，python解释器会默认调用__del__()函数
  ### 12.4 继承
  ### 12.5 重写
  ```
    class Car():
      def __init__(self,brand,typeName):
        self.brand = None
        self.typeName = None
      def run(self):
        print('car')
    c1 = Car()
  ```
## 十三、异常处理
  ```
    import traceback
    try:
    except Exception as err:
    print(f'{err}')
      print(trackback.format_exc())
  ```