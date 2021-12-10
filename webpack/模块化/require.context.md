# require.context
```js
/*
* directory(String) 文件路径
* [includeSubdirs](Boolean) 是否查找子目录
* [filter](RegExp) 默认值是 /^\.\/.*$/，所有文件
* [mode](String) 定义加载方法，可选值包括sync,eager,weak,lazy(异步加载),lazy-once
*/
// require.context(directory,includeSubdirs,filter,mode)
// 使用步骤
testList = []
const files = require.context('./compPool/', true, /attr.js$/)
files.keys().forEach(item => {
  const defaultFn = files(item).default
  this.testList.push(defaultFn)
  console.log(this.testList)
});
/*
* files.keys() 执行完返回一个存储匹配文件路径的数组
* files.default // 获取到 当前文件 导出的 默认 模块
*/
```
# 应用场景：
#### 一：组件模块化
[基础组件的自动化全局注册](https://cn.vuejs.org/v2/guide/components-registration.html#%E5%9F%BA%E7%A1%80%E7%BB%84%E4%BB%B6%E7%9A%84%E8%87%AA%E5%8A%A8%E5%8C%96%E5%85%A8%E5%B1%80%E6%B3%A8%E5%86%8C)
使用require.context()完成全局组件注册，省去了import的工作,或者我们也可以使用common.js中的require()函数来实现组件注册
例如：
```js
function getName (str) {
  return str.split('/')[0].charAt(0).toUpperCase() + str.split('/')[0].slice(1)
}
export default {
  installComp (Vue) {
    const components = require.context('./components/', true, /\.vue$/)
    components.keys().forEach(item => {
      const name = getName(item.replace(/\.\//, '').replace(/\.vue$/, ''))
      Vue.component(name, components(item).default)
    })
  }
}
// 然后在main.js文件中引入并使用即可
installComp () {
  components.installComp(Vue)
}
```
```js
// 使用require()
Vue.component(item.name, resolve => require([`./compPool/${item.name}/index`], resolve))
```
#### 二：路由模块化
```js
const routerList = []
installRouter () {
  const list = require.context("../routes", true, /\.routes\.js/)
  list.keys().forEach(item=>{
    routerList.push(list(item).default)
  })
}
installRouter()
const routes = [
    ...routerList,
];
const router = new VueRouter({
  ...routes
})
export default router
```
#### 三：store的mutations模块化
```js
// https://webpack.js.org/guides/dependency-management/#requirecontext
const modulesFiles = require.context('./modules', true, /\.js$/)

// you do not need `import app from './modules/app'`
// it will auto require all vuex module from modules file
const modules = modulesFiles.keys().reduce((modules, modulePath) => {
  // set './app.js' => 'app'
  const moduleName = modulePath.replace(/^\.\/(.*)\.\w+$/, '$1')
  const value = modulesFiles(modulePath)
  modules[moduleName] = value.default
  return modules
}, {})
```
