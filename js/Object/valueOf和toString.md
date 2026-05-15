# ({}) == '[object Object]'
其中发生的转化,你是不是一直在为没有机会使用Object.prototype.valueOf()和toString()而烦恼
valueOf()返回值为该对象的原始值。在这里它会将== 两边的类型转化为统一类型后再作比较。
### 两边类型不同时：
(1)其中一边为对象，另一个为数字或者字符串：
**会使用对象的valueOf()和toString()方法将对象转化为原始值。**
(2)数字与字符串比较，会尝试将字符串转化为数字。
(3)其中一边为Boolean,会将布尔操作符转化为1或者0
### 特殊情况：null == undefined,会返回true

[!参考文章]https://baijiahao.baidu.com/s?id=1779855819817884288&wfr=spider&for=pc
# Object.prototype.toString,
  将**对象**转换为一个原始值,该方法由字符串优先调用，但是**数字的强制转换(数学运算)**和**原始值的强制转换**会优先调用**valueOf()**
  ```js
    let arr = [1,2,3]
    console.log(Object.prototype.toString.call(arr)); //[object Array]
    console.log(arr.toString(), typeof arr.toString()); // '1,2,3' string

    let obj = {
      user:"lisa",
      valueOf: function () {
        console.log('valueOf执行了')
        return true
      },
      toString: function () {
        console.log('toString执行了')
      }
    }
    let arr = [1,2,3]
    console.log(String(obj)) // [object Object]
    console.log(100 + obj)
  ```
# valueOf和toString
  涉及知识点：数据类型转换和面向对象的原型和原型链
  - 强制类型转换使用toString()，===不会发生类型转换
    ```js
      let num = 100
      console.log(num.toString(), typeOf num.toString())
    ```
  # (2)隐式类型转换通过隐式调用String()
  原型链查找分析：
  ```js
    function test () {}
    console.log(test.prototype)  // {}
    console.log(test.toString()); // 'function test () {}'
    test --> test.__proto__ -->  
  ```
  - valueOf和toString()的使用场景：
    当我们**需要将对象进行数学运算或者转换为字符串的时候**，valueOf和toString会帮我们**将对象**转换为**能让JS计算的基本数据类型**
# 类型转换
  - 强制类型为字符串类型时会使用toString()
  - 隐式类型转换，通过隐性的调用String()、Number()、Boolean()等函数来进行转换 
对象转字符串：  toString()  --> 产物为基本类型时 -->  String()
-                           --> 不是基本类型  -->  valueOf() --> valueOf的返回值为对象时  --> toString()
  ```js
    let obj = {
      user:'lisa',
      valueOf: function () {
        console.log('valueOF');
        return {}
      },
      toString: function () {
        console.log('toString');
        return '20'
      }
    }
    // console.log(String(obj));
    console.log(100 + obj); // 101

    // =============习题===================
     var a = {
      _default: 0,
      valueOf: function () {
        console.log('valueOf');
        return 4
      },
      toString: function () {
        console.log('toString');
        return ++ this._default
      }
    }
    // 让== 隐式转换的时候改变a的值
    if (a == '1' && a == '2' && a == '3') {
      console.log('成立了！')
    } // 隐式转换为字符串：toString()  --> 产物为基本类型 --> String()
  ```

# 
```js
console.log({}.toString())//[Object,Object]
console.log([].toString()) // ''
console.log([1,2,3].toString()) // '1,2,3'
console.log(({} + {}).length)
console.log(([] + []).length)
console.log(function(){}.toString()) // ‘function(){}’
console.log(function(){}.length) // 0
console.log(function(a,b,c){}.length) // 3
```