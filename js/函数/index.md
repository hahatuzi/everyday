# 函数和Function的关系
  - 在js中**每一个函数**其实**都是一个Function对象**，**Function对象**提供了用于处理**函数**的方法。
# Function对象
  - **Function()构造函数**创建了一个新的**Function对象**，直接调用**该构造函数**的话**可以动态创建函数**。
  - 而通过自定义名字的构造函数创建的实例则和Function无关。比如 f1 = new Foo()和f = new Function()，分别指向不同的构造函数

# Function和自定义构造函数
# Function构造函数和函数声明的不同:Function构造函数创建的是全局环境，和函数声明不同
  ```js
    // 注意点：
    // new Function()的作用域引用的是全局环境，而非包含该函数的外部环境，所以他们不会使用外部环境中的变量,即它不会创建闭包环境！！！
    var a = 1
    var b = 2
    var c = 4
    function test2 () {
      var a = 2
      return new Function('c','console.log(a + b + c)')
    }
    function test3 () {
      const c = 5
      function fn() {
        console.log(a + b +c)
      }
      return fn
    }
    var res = test2()
    var res1 = test3()
    res(4) // 7
    res1(4) // 8
  ```
# new Foo和new FOO()的区别

# Function和Object

# 一：函数的六种创建方式
  ### （1）直接声明函数并调用
    ```js
      function sayHello () {
        console.log('sayHello')
      }
      sayHello()
    ```

  ### （2）函数表达式，通过变量名来调用该函数
    ```js
      const sayHello = function () {
        console.log('sayHello')
      }
      sayHello()
    ```

  ### （3）箭头函数
    ```js
      const sayHello =() => {
        console.log('sayHello')
      }
      sayHello()
    ```

  ### （4）构造函数，通过new关键字来调用
    ```js
      function SayHello () {
        console.log('sayHello')
      }
      const s = new SayHello()
    ```
  
  ### （5）立即调用函数，就是当它被定义出来时就会自动执行的函数，不需要调用
    ```js
      (function  () {
        console.log('sayHello')
      })()
      // 写法一
      (
        function (参数) {函数方法}
      ) (给参数的值)
      // 写法二
      (
        function (参数) {函数方法} (给参数的值)
      )
      // 写法三
      ！function(参数) {函数方法} (给参数的值)
      // 注：自执行函数的内部可以访问全局变量，但是除了自执行函数自身内部，是无法访问到它的。
    ```
  
  ### （6）Function构造函数
    ```js
      // var fn = new Function(形参列表， 函数体)
      const sum = new Function(a,b, 'return a + b')
      console.log(sum(1,2))
      // function Foo(){}等于 var Foo = new Function()
    ```

  ### 构造函数 VS 函数声明 VS 函数表达式
    ```js
      var multiply = new Function("x", "y", "return x * y");
      function multiply(x, y) { return x * y }
      var multiply = function (x, y) { return x * y; };

    ```

# 二：函数调用的四种方法：作为对象方法调用，函数调用模式，构造器调用模式，apply,call调用模式
  **注**this指向问题的本质就是确定该函数的调用者，确定该函数所处的调用域
  ### （1）作为对象方法调用,this指向该对象
    ```js
      // 先定义一个对象，然后在对象的属性中定义方法，通过myobject.property来执行方法，this即指当前的myobject对象。
      var blogInfo = {
      　　blogId:123,
      　　blogName:"werwr",
      　　showBlog:function(){alert(this.blogId);}
      };
      blogInfo.showBlog(); // 函数的调用者为blogInfo,所以此处的this就是blogInfo的区域
    ```

  ### （2）函数调用模式, this指向window
    ```js
      // 定义一个函数，设置一个变量名保存函数，这时this指向到window对象。
      var myfunc = function(a,b){
      　　return a+b;
      }
      alert(myfunc(3,4));// 无调用者，因为该函数没有调用者，所以this默认指向window，结果为7，但严格模式下结果为undefined
    ```

  ### （3）构造器调用模式
    ```js
      // 定义一个函数对象，在对象中定义属性，在其原型对象中定义方法。在使用prototype的方法时，必须实例化该对象才能调用其方法。
      var myfunc = function(a){
      　　this.a = a;
      };
      myfunc.prototype = {
      　　show:function(){alert(this.a);}
      }

      var newfunc = new myfunc("123123123");
      newfunc.show();
    ```

  ### （4）间接调用模式
    ```js
      var myobject={};
      var sum = function(a,b){
      　　return a+b;
      };
      var sum2 = sum.call(myobject,10,30); // 会将this指向myobject
      alert(sum2);
      var sum3 = sum.apply(myobject,[10,30]); // 会将this指向myobject
      alert(sum3);
    ```
    ```js
      // 注这两种调用模式和bind()的区别在何处,apply和call都直接返回函数调用的结果，但是bind的返回值是一个新的函数。
        var obj = {};
        var btn = document.querySelector('button');
        btn.onclick = function () {
            console.log(this); // 没点击不会输出{}
        }.bind(obj); 
        btn.onclick = function () {
            console.log(this); // 没点击也会输出{}
        }.call(obj); //或.apply(obj); 
    ```
    ```js
      window.onload = function () {
        var length = 88;
        function test() {
          console.log(this.length) 
        }
        test()// 因为该函数没有调用者，所以this默认指向window，结果为88，但严格模式下结果为undefined
        var obj = {
          length: 99,
          action: function (test) {
            test();
            arguments[0]() // this指向arguments，因为argument为调用者。
          }
        }
        obj.action(test, [1, 2, 3])
      }
    ```
    ```js
      // 例题二：改变this指向
      function bindThis (fn, target) {
        return function () {
          return fn.apply(target, arguments)
        }
      }
    ```

# 三：默认参数，默认参数的注意事项：
  ### （1）默认位置：默认参数值的位置最好是最后一位。
    ```js
      function fn (a,b = 1){
        console.log(a + b)
      }
      fn(2)
      function fn (a = 2,b){
        console.log(a + b)
      }
      fn(undefined, 2)
    ```
  ### （2）默认参数对函数的length属性的影响，**添加了默认参数后会导致函数的length只返回默认参数之前的形参个数**
    ```js
      function fn (a, b = 1, c){
        console.log(a + b +c)
      }
      console.log(fn.length)
    ```
  ### （3）每次重新调用函数时默认参数都会重新赋值
  ### （4）默认参数可以和形参一起结合使用
    ```js
      function fn (a, b, c = (a + b)){
        console.log(a, b, c)
      }
      fn(1,2)
    ```

# 四：形参，函数形参为对象时，形参指向引用地址
  ```js
    function change (obj) {
      console.log(obj.name)
      obj.name = 'lili'
      console.log(obj.name)
      console.log(obj)
    }
    change(person)
    console.log(person) // {name:'lili'}
  ```
  
# 五：arguments,函数的所有实际参数会被保存在arguments对象中，arguments是一个类似数组的对象
  ```js
    // 实参求和
    function test(a,b,c,d,e){
      b = 9 // 形参和实参的关系，argumeent[0] --> a 映射关系
      arguments[2] = 0
      console.log(arguments,c,arguments[2])
    }
    test(1,2,3)
    // arguments可以迭代
    function myConcat(separator) {
      console.log(typeof arguments) // object
      console.log(arguments instanceof Array) // false
      console.log(arguments instanceof Object) // true
      let result = ""; // 初始化列表
      // 迭代 arguments
      for (let i = 1; i < arguments.length; i++) {
        result += arguments[i] + separator;
      }
      return result;
    }
    console.log(myConcat("、", "红", "橙", "蓝"));
    // "红、橙、蓝、"
  ```
# 五：函数的prototype原型,原型链，instanceof
  ### 为什么只有函数有protype
  https://developer.aliyun.com/article/977147
  ### instanceof
   - instanceof 运算符用于检验**构造函数的prototype属性**是否出现在**某个示例对象**的**原型链**上。
   - 如果表达式obj instanceof Foo返回true,则并不意味着该表达式会永远返回 true。因为 Foo.prototype 属性的值有可能会改变，**改变之后的值很有可能不存在于 obj 的原型链上**，这时原表达式的值就会成为 false。另外一种情况下，原表达式的值也会改变，就是改变对象 obj 的原型链的情况，虽然在目前的 ES 规范中，我们只能读取对象的原型而不能改变它，但借助于非标准的 __proto__ 伪属性，是可以实现的。比如执行 obj.__proto__ = {} 之后，obj instanceof Foo 就会返回 false 了。
    ```js
      let test = function (){}
      console.log(test instanceof Function) //true
      console.log(b instanceof Object)
      console.log(undefined instanceof Object)

      function A () {}
      A.prototype.n = 1
      let a1 = new A()
      A.prototype = {
        n: 2,
        m:3
      }
      let a2 = new A()
      console.log(a1.n, a1.m, a2.n, a2.m,)
    ```
# Function
  - Function.prototype.prototype在使用function作为构造函数与new运算符一起使用时，用作新对象的原型
  - Function.prototype.toString()返回表示函数源代码的字符串。重写了 Object.prototype.toString 方法。
  - Function和自定义构造函数的关系

# 变量提升和函数提升,即预编译
  - 变量提升：通过**var定义**的变量，在定义语句之前就可以访问到，值为**undefined**
  - 函数提升：通过**function声明**的函数，在之前就可以直接调用，值为**函数本身**
  - 当同时使用var和function定义**同名变量**时，会**先调用function变量提升，后调用var变量提升**，提升后的结果就变成了undefined
  - 如果函数是通过var定义的，那么它就属于变量提升
    ```js
      var a = 3
      function fn (){
        console.log(a)
        var a = 4
        console.log(b) // Cannot access 'b' before initialization
        let b = 3
      }
      console.log(fn1) // undefined
      fn1() //此处遵循的是变量提升,fn1 is not a function
      var fn1 = function () {
        console.log('fn1')
      }
      fn()
      // =============
      // 当同时使用var和function定义同名变量时，会先调用function变量，后调用var变量
      var c = 1
      function c(c){
        console.log(c)
      }
      c(2)// c is not a function
      // ================
      function fn () {
        obj={name: 'lisa'}
      }
      console.log(obj)
    ```
# 执行上下文和作用域
  ### 全局执行上下文：在执行全局代码前将**window**作为全局执行上下文。
  - 对全局数据进行预处理：var定义的全局变量-->undefined,添加为window的属性
  - function声明的全局函数-->复制为fun,添加为window的方法
  - this --> window
  - 开始执行全局代码
  ### 函数执行上下文，在调用函数且准备执行函数体之前，创建对应的函数执行上下文对象。
   - 对局部数据进行预处理
   - 形参变量 --> 赋值（实参）--> 添加为执行上下文的属性
   - arguments --> 赋值（实参列表）-->添加为执行上下文的属性
   - var定义的局部变量 --> 赋值undefined-->添加为执行上下文的属性
   - function定义的函数 --> 赋值fun-->添加为执行上下文的属性
   - this --> 调用函数的对象
  ### 作用域和执行上下文的区别
   - 作用域是静态的，只要函数定义了就会存在且不会再变化，执行上下文会随着函数的调用结束被释放
   - 上下文对象从属于所在的作用域，全局上下文环境-->全局作用域，函数上下文环境-->对应的函数作用域
   ```js
     var x = 10
     function fn () {
      console.log(x)
     }
     function show (f) {
       var x = 20
       f()
     }
     show(fn)
   ```
  