# for...in和for..of
###　for...in,
以任意顺序遍历一个对象的除Symbol以外的**可枚举属性**，**包括继承的可枚举属性**
**会遍历到原型上的方法，所以在遍历的时候常常用Object.hasOwnPropery判断一下是否是该对象的实例对象。**
```js
Object.prototype.fn = function () {
  console.log('原型fn')
}
var obj1= {
  name: 'lisa'
}
for (var key in obj1) {
  if (obj1.hasOwnProperty(key)) {
    console.log(key)
  }
}
```
**注：不建议使用for in  去遍历更关注索引的数组**

### for...of
在**可迭代对象**(Array,Map,Set,String,arguments)上创建一个迭代循环
```js
(function () {
  for (let argument in arguments){
    console.log(argument)
  }
})(1,2,3)
```
### 区别：
for in 遍历的是对象的可枚举属性，而for of 遍历的是可迭代对象，这意味着这个对象（或其原型链中的任意一个对象）必须具有一个带 Symbol.iterator 键（key）的属性。内置的可迭代对象包括String,Array,Map,Set