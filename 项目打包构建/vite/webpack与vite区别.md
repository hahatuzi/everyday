# 1.构建流程对比：
  - webpack
    entry -->  route1  --> module  --> bundle -->   server ready
          -->  route2  --> module
          -->  route3  --> module (等所有的模块都构建完成后才bundle)
  - vite
    server ready -->  route1  --> module (按需构建路由对应的模块)
                 -->  route2  --> module
                 -->  route3  --> module

# 2.批量引入文件的区别，
```js
// 首先是webpack中
// require.context(directory, useSubdirectories, regExp)
// directory: 要查找的文件路径
// useSubdirectories: 是否查找子目录
// regExp: 要匹配文件的正则
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
// 上述方法会返回一个对象
// 而在vite中是这样引入的
// import.meta.globEager("../components/*.vue")
// 传入一个文件路劲然后用*通配符代表此目录下的每一个文件
const modules = import.meta.globEager("./*.vue")
const componentsMoudleObj = {}
for (const key in modules) {
  let name = key.substring(key.lastIndexOf('/') + 1, key.lastIndexOf('.vue'))
  componentsMoudleObj[name] = modules[key].default
}

export default componentsMoudleObj
```