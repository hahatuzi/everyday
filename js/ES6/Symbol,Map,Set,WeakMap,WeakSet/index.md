# 一：Symbol
为了解决对象的属性名不能重复的问题，出现了Symbol,Symbol值是通过Symbol函数创建的。
 - 对象的属性名可以是**字符串**也可以是**Symbol**
 - symbol强调独一无二几个字，每个从Symbol()返回的Symbol值都是唯一的。因此可以作为对象的唯一属性名的标识符
 ### 1.Symbol()和Symbol.for()的区别
  - Symbol.for() 和 Symbol() 方法都会生成新的 symbol 类型的值.
  - 不同的是 Symbol.for() 方法会查找命名参数是否在全局中注册过，如果注册过的就不会创建新的值，而是会直接返回，所以我们可以使用到相同的 symbol 值
  - 使用 **Symbol() 方法每次都会创建一个新的值**，且不会注册到全局。

 ### 2.Symbol.keyFor()
 Symbol.keyFor() 方法表示获取一个 symbol 的值在全局中注册的命名参数 key，只有使用 Symbol.for() 创建的值才会有注册的命名参数，使用 Symbol() 生成的值则没有：

 ### 3.Symbol.toPrimitive
  [OTC]https://blog.csdn.net/xcg132566/article/details/108109837
  对象的 Symbol.toPrimitive 属性，指向一个方法。该对象被转为原始类型的值时，会调用这个方法，返回该对象对应的原始类型值。

  - Symbol.toPrimitive 被调用时，会接受一个字符串参数，表示当前运算的模式，一共有三种模式：
  - Number：该场合需要转成数值
  - String：该场合需要转成字符串
  - Default：该场合可以转成数值，也可以转成字符串


# 二：Set
- set转array
```js
const arrset = new Set([10,2,0,3,4,10,10])
console.log(Array.from(arrset))
console.log([...arrset])
```

# 三：WeakSet
- WeakSet只能存放对象类型，不能存放基本类型
- 可以被垃圾回收的值的集合，WeakSet 中对象的引用为**弱引用**。**如果没有其他的对 WeakSet 中对象的引用存在，那么这些对象会被垃圾回收**。
- 不能遍历，无法获取WeakSet中的对象
```js
  // 使用set添加的对象为强引用，obj=null后0x100堆空间内存不会被销毁，而WeakSet会销毁该空间内存
  let obj = {name:'lisa'} // 0x100
  const set = new Set() // 0x200
  set.add(obj) // set[item1]  -->  0x100
  obj = null
```

# 四：Map
  map对象保存**键值对**，并且**能够记住键的原始插入顺序**，任何类型都可以作为一个键或者值
  一个map对象 在迭代时会根据元素的插入顺序进行一个**for of**循环,在每次迭代后返回一个形式为[key,value]的数组
  ### 实例方法：
    ```js
      Map.prototype.clear() // 移除map对象中所有的键值对
      Map.prototype.delete(key) // 移除指定键值对
      Map.prototype.get(key) // 返回与key关联的值，若不存在，则返回undefined
      Map.prototype.has(key) // 返回一个布尔值，用来表明Map对象中是否存在与key关联的值
      Map.prototype.set(key, value) // 在Map对象中设置与指定的键key关联的 值value,并返回Map对象
      Map.prototype.keys(), //返回一个迭代器对象，包含按照顺序插入的元素的key值
      Map.prototype.values(), //返回一个迭代器对象，包含按照顺序插入的元素的values值
    ```

# 五：WeakMap
  - WeekMap类似于Map,都是键值对，但是WeekMap**只有对象能够作为键**，且键是弱引用的，
  - 如果一个对象只被WeakMap引用，那么这个对象**可以被垃圾回收（GC）**。当这个对象被垃圾回收后，它对应的键值对也会从WeakMap中自动移除。
  - WeekMap**不能遍历**

# 六：Set和Map的不同之处

  - **相同点**
    - set对象可以存储任何类型的唯一值，无论是原始值或者对象引用
    - map对象也可以存储任何值（对象或者基本类型）都可以作为一个键或一个值。
  - **不同点**
  set保存值，map保存键值对

# 七：方法
  |       **map**        |       **set**       |        **set**      |     **WeakSet**     |
  | -------------------- | --------------------| --------------------| --------------------|
  |      set(key, val)   |    add(value)：     |    add(value)：     |    add(value)：     |
  |      get(key)        |                     |                     |                     |
  |      has(key)        |    has(value)：     |    has(value)：     |    has(value)：     |
  |      delete(key)     |    delete(value)    |    delete(value)    |    delete(value)    |
  |      clear()         |    clear()          |    clear()          |                     |
  |      .size           |    .size            |    .size            |                     |
  |      forEach()       |    forEach()        |    forEach()        |                     |
