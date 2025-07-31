# Reflect， 它提供拦截Javascript操作的方法，这些方法和proxy的handler属性上的方法相同
我们可以将reflect看做**封装了一些底层操作逻辑**的**API**,ES6中将很多原本Object上的**属性转移到了Reflect上**，风转的目的在于代码可读性，又避免了直接操作底层对象。
```js
target[prop] = value
//等价于
Reflect.set(target, prop,value, receiver)
// receiver如果遇到setter，receiver为setter调用时的this
//=========================
target[prop]
// 等价于
Reflect.get(target,prop)
```

### 附录一.reflect的静态方法列表
|              静态方法              |                   调用方式                 |
| ---------------------------------- | -------------------------------------------|
|            Reflect.get             |                   读取属性                 |
|            Reflect.set             |                   新增属性                 |
|            Reflect.has             |                   in操作符                 |
|            Reflect.apply           |                 调用一个函数               |
|            Reflect.construct       |                      new                   |
|        Reflect.defineProperty      |          Object.defineProperty             |
|      Reflect.deleteProperty        |               delete操作符                 |
|        Reflect.getPropertyOf       |          Object.getPropertyOf              |
|        Reflect.setPropertyOf       |          Object.setPropertyOf              |
|        Reflect.isExtensible        |           Object.isExtensible              |
|     Reflect.preventExtensions      |        Object.preventExtensions            |
|      getOwnPropertyDescriptor      |       Object.getOwnPropertyDescriptor      |
|          Reflect.ownKeys           |  Object.keys( ) \ Object.getOwnPropertyNames( ) \ Object.getOwnPropertySymbols( )  |