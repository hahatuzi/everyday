# 1.call，apply，bind区别
  个人理解的为什么会出现call，apply之类的方法呢，我们都知道它们都是**为了改变this指向，即改变函数作用域**，那么为什么还会存在差异呢
  （1）传参不同，call(target,arg1, arg2),apply(target, [args]),bind(target,arg1,arg2,...)
  （2）返回值不同
  call和apply返回值都是**调用函数的结果**，而bind返回值则是**调用函数的副本**
  （3）bind的执行过程：
  **创建一个新函数** --> **将新函数传入的参数**存储为**新函数** 的**内部状态** --> **新函数执行目标函数,目标函数指绑定函数包装的函数**
  ```js
    const boundFn = fn.bind(obj, arg1,arg2)
    const boundFn = (...restArgs) => fn.call(obj, arg1, arg2, ...restArgs) // 等价

    // 案例一
    function log (...args){
      console.log(this, ...args)
    }
    let obj = {name:'lisa'}
    const boundLog = log.bind(obj, 1,2) // 先创建新函数boundLog，再将3,4作为boundlog函数的传参
    boundLog(3,4)
    // 等价于
    const boundLog = (3,4) => log.call(obj, 1, 2, 3, 4)

    // 案例二
    function log (...args){
      console.log(this, ...args)
    }
    let obj = {name:'lisa'}
    let newobj = {name:'rose'}
    const boundLog = log.bind(obj, 1,2)
    const boundLog2 = boundLog.bind(newobj, 3,4)
    boundLog2(5,6)
    // 等价于
    const buoundLog = () => log.call(obj, 1 , 2)
    const boundLog2 = (5,6) => boundLog.bind(newobj, 3,4)
  ```
# 2.代码实现过程
```js
    // 手撕bind
    let obj = {name:'lisa'}
    function createPerson (...args) {
      console.log(this.name, ...args)
    }
    Function.prototype.bind_self = function (obj, ...args){
      let fn = this // 获取调用bind_self的调用函数，这里指createPerson
      // 返回值为函数
      return function (...params) {
        console.log(obj, args, params)
        // 将函数挂在新对象上
        fn.call(obj,...args, ...params) // 修改调用函数中this的指向
      }
    }
    let fn2 = createPerson.bind_self(obj, 'a', 'b')
    // fn2( 'c', 'd', 'e')
    let fn3 = fn2.bind(obj1,  'c', 'd', 'e')
    fn3('f', 'g')
```
# 3.应用场景
（1）类数组转化[].slice.call(childNodes)
（2）判断是否有某个属性Object.hasOwnProperty.call(obj, 'name')