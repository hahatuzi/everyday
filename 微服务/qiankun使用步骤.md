# 使用步骤
```js
// 第一步：引入qiankun
import { registerMicroApps, start } from 'qiankun';
// 第二步：注册子应用
const apps = [
  {
    name:'sub-react', // 子应用的名称
    entry:'//localhost:3001', // 默认会加载这个路径下的htm，解析里面的js
    activeRule:'#/sub_react',
    container:'#sub_app', //加载的容器
    // 主应用和子应用之间传参
    props:{
      publicPath:'/sub_react'
    }
  }
]
registerMicroApps(apps, {
  beforeLoad:[async app => console.log('boforeLoad', app.name)],
  beforeMount:[async app => console.log('beforeMount', app.name)],
  beforeUnmount:[async app => console.log('beforeUnmount', app.name)],
})
 // 第三步：启动微服务
start()
```
当微应用信息注册完成后，一旦浏览器的**URL发生变化**，就会**自动触发qiankun的匹配逻辑**，所有**activeRule**规则匹配上的微应用就会**被插入到指定的contaienr中**，**同时一次调用微应用中的暴露的生命周期钩子函数**


# react子应用改造
为了不eject所有的配置，我们选择用react-app-rewires工具来改造webpack配置
### 1.bootsrap生命周期
bootstrap生命周期：只会在微应用初始化时调用一次，下次重新进入时会直接调用mount方法。
# 常见问题：
### 问题一：样式隔离
qiankun实现了各个自应用之间的样式隔离，但是基座和子应用之间的样式隔离没有实现，所以基座和子应用之间还会存在样式冲突，比如ant-design
解决方案：通过css-modlue给咩个模块加上前缀
### 问题二：子应用之间的跳转
（1）情形一：主应用和子应用都是hash模式的话，主应用根据hash来判断微应用
（2）情形二：history模式，因为微应用的路由实例跳转是基于路由的base的，所以可以通过history.pushState()或者主应用通过路由实例将props传给微应用。
```js
const _wr = function (type) {
  const orig = (window).history[type]
  return function () {
    const rv = org.apply(this,arguments)
    const e = new Event(type)
    e.arguments = arguments
    window.dispatchEvent(e)
    return rv
  }
}
window.history.pushState = _wr(['pushState'])
```
# 公共依赖加载
一般来说，各个子应用是通过业务来划分的，不同业务线应该降低耦合度，尽量去避免通信，但是如果涉及到一些公共的状态或者操作，qiankun也是支持的。
qinkun提供了一个全局的Globalstate来共享数据，基座初始化之后，子应用可以监听到这个数据的变化，也能提交这个数据
基座:
// 基座初始化
```js
import { initGlobalstate } from 'giankun';
const actions = initGlobalState(state);// 主项目项目监听和修改
actions.onGlobalStateChange((state， prev) => (// state:变更后的状态; prev 变更前的状态
console.log(state, prev);
))
actions.setGlobalState(state);
```
子应用
// 子项目监听和修改
```js
export function mount(props) {
props.onGlobalStateChange((state，prev) => (// state:变更后的状态; prev 变更前的状态console.log(state, prev);
props.setGlobalState(state);
}
```