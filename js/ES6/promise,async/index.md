# 一：错误
  ### 错误常见类型：
  - ReferenceError:对象代表当一个不存在的变量被引用时发生的错误
  - SyntaxError：语法错误
  - TypeError: 类型错误

# 二：promise
  ### 1.状态：
  - （1）pending //待定
  - （2）fulfilled //已兑现(以一个值的形式被兑现)
  - （3）rejected // 已拒绝（以一个原因形式被拒绝） 
  ### 2.promise的优缺点：
  - （1）指定回调函数的方式更加灵活：
  旧的回调函数：只能在启动异步任务启动前指定回调函数。
  它可以异步任务开启后创建promise对象成功后绑定回调函数，也可以在异步任务结束后指定。
  - （2）支持链式调用，解决了回调地狱的不便于阅读和不方便处理异常的缺点。
  - （3）缺点：无法取消Promise，一旦新建它就会立即执行，无法中途取消。其次，如果不设置回调函数，Promise内部抛出的错误，不会反应到外部。当处于Pending状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）
  ```js
    promise.then(
          console.log('test')//同步
        ).then(res => {
          console.log('fulfilled') //根据resolve的时间而定
          return Promise.resolve('fulfilled')
          }).then(value => {
          console.log(value, 'oo') //同步
          return new Promise((resolve, reject) => {
            setTimeout((data) => { 
              // reject('Error')
              resolve('fulfilled2000')
            }, 2000)
          }) //异步
        }).then(value => {
            setTimeout(() => {
              console.log(value, 'pm')
            }, 5000)
          })
          .then(value => { console.log(value, 'pm') })
          // undefined,'pm'
          // fulfilled2000,'pm'
  ```
 ### 3.promise的all,race,
 ### 3.手写promise