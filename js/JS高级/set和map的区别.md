# 1.存储值
**相同点**
set对象可以存储任何类型的唯一值，无论是原始值或者对象引用
map对象也可以存储任何值（对象或者基本类型）都可以作为一个键或一个值。
**不同点**
set保存值，map保存键值对
# 2.方法
|         map          |         set         |
| -------------------- | --------------------|
|      set(key, val)   |    add(value)：     |
|      get(key)        |                     |
|      has(key)        |    has(value)：     |
|      delete(key)     |    delete(value)    |
|      clear()         |    clear()          |
|      .size           |    .size            |
|      forEach()       |    forEach()        |