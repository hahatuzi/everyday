# requireJS
## 一：为什么要使用requireJS
为了解决一次加载多个js文件时网页停止渲染的问题。而且当js文件间互相依赖时还要保证相互之间的加载顺序的问题。
所以它实现了以下两个功能：
(1)实现了js文件的异步加载，避免网页失去响应
(2)管理模块之间的依赖性，便于代码的编写和维护。
## 二：主模块和依赖模块
**主模块**
我们在引入require.js后使用data-main属性来指定网页的主模块,比如
```js
<script src="js/require.js" data-main="js/main"></script>
// 指定main.js为主模块入口，因为reuqire.js默认的文件后缀名就是js，所以可以把main.js简写为main.
```
**依赖模块**
依赖模块的意思是被主模块依赖的其他模块，使用方法：通过AMD规范的require()函数
```js
/*
*参数一：array,表示所依赖的模块
*callback,加载的模块会以参数形式传入该函数，从而在回调函数内部可以使用这些模块。
*/
require(['moduleA','moduleB']),function(moduleA,moduleB){})
```

## 三：应用场景：vue异步组件
```js
Vue.component('async-example', function (resolve, reject) {
  setTimeout(function () {
    // 向 `resolve` 回调传递组件定义
    // 你也可以调用 reject(reason) 来表示加载失败
    resolve({
      template: '<div>I am async!</div>'
    })
  }, 1000)
})
// 模块写法
// 这是本来的写法，然后我们使用require.js将组件作为模块来管理
Vue.component('async-webpack-example', function (resolve) {
  // 这个特殊的 `require` 语法将会告诉 webpack
  // 自动将你的构建代码切割成多个包，这些包
  // 会通过 Ajax 请求加载
  require(['./my-async-component'], resolve)
})
// 动态写法
Vue.component(
  'async-webpack-example',
  // 这个动态导入会返回一个 `Promise` 对象。
  () => import('./my-async-component')
)
// 那么我们的模块写法和动态写法的区别在哪里呢？我们将在四中探讨一下
```
## 四：异步组件和动态组件的区别
（1）使用动态import导入的话，项目打包会将所有component打包在一个js文件中，从而导致首页加载内容太多，时间较长。
（2）require导入的时候会分别打包成不同的js，加载也是按需加载。