# for...in和for..of
1.遍历对象
(1)for...in,
以**任意顺序**遍历一个对象的除Symbol以外的可枚举属性，包括继承的可枚举属性
会遍历到原型上的方法，所以在遍历的时候常常用Object.hasOwnPropery判断一下是否是该对象的实例对象。
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

2.遍历数组
for...of在**可迭代对象**(Array,Map,Set,String,arguments)上创建一个迭代循环