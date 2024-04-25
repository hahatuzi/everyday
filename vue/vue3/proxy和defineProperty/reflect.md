# Reflect,
我们可以将reflect看做**封装了一些底层操作逻辑**的**AP**I,ES6中将很多原本Object上的**属性转移到了Reflect上**，风转的目的在于代码可读性，又避免了直接操作底层对象。
```js
target[prop] = value
//等价于
Reflect.set(target, prop,value)
target[prop]
// 等价于
Reflect.get(target,prop)
```