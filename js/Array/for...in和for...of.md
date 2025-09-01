# 一：for...in和for..of
  ###　(1)for...in,迭代对象的所有可枚举属性，包括继承的可枚举属性
    ```js
    // 以任意顺序遍历一个对象的除Symbol以外的可枚举属性**，**包括继承的可枚举属性**
    // 会遍历到原型上的方法，所以在遍历的时候常常用Object.hasOwnPropery判断一下是否是该对象的实例对象。
      Object.prototype.fn = function () {
        console.log('原型fn')
      }
      var obj1= {
        name: 'lisa'
      }
      for (var key in obj1) {
        if (obj1.hasOwnProperty(key)) {
          console.log(key) // fn, name
        }
      }
    ```
  **注：不建议使用for in  去遍历更关注索引的数组**

  ### (2)for...of,循环处理可迭代对象的值序列
    ```js
      // 在**可迭代对象**(Array,Map,Set,String,arguments)上创建一个迭代循环
      (function () {
        for (let argument in arguments){
          console.log(argument)
        }
      })(1,2,3)
    ```
  ### (3)区别：
  for in 遍历的是对象的可枚举属性，而for of 遍历的是可迭代对象，这意味着这个对象（或其原型链中的任意一个对象）必须具有一个带 Symbol.iterator 键（key）的属性。内置的可迭代对象包括String,Array,Map,Set
  ### (4)迭代器
    ```js
      // 生成器：生成返回一个迭代器
      function * generotor (arr) {
        for (const key of arr) {
          yield key
        }
      }
      const iterator = generotor([1,2,3,4,5])
      console.log(iterator.next())
      console.log(iterator.next().value)
      console.log(iterator.next().value)

      // 自定义实现迭代器
      const o = {
        0:1,
        1:2,
        2:3,
        length:3
      }
      Object.prototype[Symbol.iterator] = generotor
      function generotor () {
        var _this = this
        let nextIndex = 0
        return {
          next () {
            return nextIndex < _this.length ? {value:_this[nextIndex++], done:false} : {value:undefined, done:true}
          }
        }
      }
      for (const v of o) {
        console.log(v)
      }
    ```