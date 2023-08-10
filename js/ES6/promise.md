#### 1.区别实例对象和函数对象
```js
function Fn(){}
Fn.call() //此时Fn为函数对象，因为它此时是作为对象调用call属性的目的
var f1 = new Fn() //实例对象
```
#### 2.回调函数的分类：同步回调和异步回调
```js
console.log(1)
var arr = [0,1,2,2]
arr.forEach(item=>{
// 同步回调
  console.log(2)
})
console.log(3)
console.log(1)
var arr = [0,1,2,2]
arr.forEach(item=>{
// 异步回调
setTimeout(item=>{
  console.log(3)
},0)
})

console.log(2)
```
#### 3.错误处理的方法
错误常见类型：
ReferenceError:对象代表当一个不存在的变量被引用时发生的错误
SyntaxError：语法错误
TypeError: 类型错误
(1)try..catch // 捕获错误
(2)throw // 抛出一个用户自定义的异常
(3)try catch和promise.catch的区别
##### 1.try..catch语法捕获同步任务产生的错误
##### 2.promise.catch()捕获异步任务产生的错误
#### 4.对promise的理解
(1)高层次来看：promise是一种新的用来执行异步编程的解决方式。旧的是回调函数方式。
(2)语法来看：promise是一个构造函数，用来封装异步操作并获取其结果。
#### 5.promise的状态及状态改变
一：状态：
（1）pending //待定
（2）fulfilled //已兑现(以一个值的形式被兑现)
（3）rejected // 已拒绝（以一个原因形式被拒绝）
二：状态改变：
pending-->fulfilled-->.then(onfulfillment)-->async actions
                                          -->return Promise
pending-->rejected-->.then(onRejection)/.catch(onRejection)-->async actions
                                                           -->return Promise
![在这里插入图片描述](https://img-blog.csdnimg.cn/2577bc5908224fff8777e9ab1f32d269.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA5Yav6Zi_5a6d,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

```js
function bindUser(data,successCallback,errorCallback){
  const _data = data
  const promise = new Promise((resolve,reject)=>{
    const res = await registerCrm(data)
    if res.code === 0 {
      resolve(res.data)
    } else {
      reject(res.message)
    }
  })
  promise.then(
      return new Promise((resolve,reject)=>{
      const res = await dataTrackCb(data)
      if res.code === 0 {
    resolve(res.data)
  } else {
    reject(res.message)
  }
    }))
    .then(()=>successCallback(value))
    .catch(()=>errorCallback(error))
}
```
#### 6.promise的优缺点：
1.指定回调函数的方式更加灵活：
旧的回调函数：只能在启动异步任务启动前指定回调函数。
它可以异步任务开启后创建promise对象成功后绑定回调函数，也可以在异步任务结束后指定。
2.支持链式调用，解决了回调地狱的不便于阅读和不方便处理异常的缺点。
缺点：无法取消Promise，一旦新建它就会立即执行，无法中途取消。其次，如果不设置回调函数，Promise内部抛出的错误，不会反应到外部。当处于Pending状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）
#### 7.promise的同步异步：
.then()可以返回同步或者异步的操作，如果要返回异步的操作需要用promise包裹起来。
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
.then()的返回值类型：
数值，空，错误，promise的pending状态(异步)，fulfilled状态，rejected状态
```js
promise.then(()=>{
return 3 //
throw new Error()
return Promise.resolve()
return Promise.reject()
return new Promise() //异步
})
```
8.promise的异常传递：
当使用promise的then链式调用时可以在最后指定失败的回调
9。中断promise链
then返回一个promise的pending状态

## async和await
```js
async function fn(){
return 1
}
var f1 = fn()
console.log(f1)//Promise对象 
// await的右边是一个promise对象，得到的是promise的成功结果的value，promise的失败结果需要通过try。。。catch获取
```
## JS异步之宏队列和微队列
