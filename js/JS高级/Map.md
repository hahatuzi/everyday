# map对象保存键值对，并且能够记住键的原始插入顺序，任何类型都可以作为一个键或者值
# 一个map对象 在迭代时会根据元素的插入顺序进行一个for of 循环在每次迭代后返回一个形式为[key,value]的数组
```js
const map1 = new Map()
map1.set('a', 0)
```
# 实例方法：
```js
Map.prototype.clear() // 移除map对象中所有的键值对
Map.prototype.delete(key) // 移除指定键值对
Map.prototype.get(key) // 返回与key关联的值，若不存在，则返回undefined
Map.prototype.has(key) // 返回一个布尔值，用来表明Map对象中是否存在与key关联的值
Map.prototype.set(key, value) // 在Map对象中设置与指定的键key关联的 值value,并返回Map对象
```