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

# vite的特点
  - 编译方面：vite利用esm，让代码不再像传统的构建工具一样先去分析引入，然后打包构建。而是**直接保持模块化**，省去了编译时间。
  - 构建方面，vite采用rollup，vite本质就是走一步看一步，而webpack是刚开始就扫描整个项目进行打包编译。

  # vite不需要再像webpack一样配置各种loader,比如css文件打包需要css-loader,scss-loader等loader配置

  # HMR热更新：webpack改一行代码需要重新解析它的依赖，导致启动慢，HMR慢。
  # vite处理案例：请求main.ts --> import APp.vue -->  使用vitejs/plugin-vue编译 --> 返回js模块

# vite和webpack的HMR的区别
  |              |             vite HMR                  |              Webpack HMR                |
  |   运行方式   |             基于原生ESM模块           |              基于webpack依赖图          |
  |   更新机制   |           按需更新，直接替换模块      |          需要构建整个模块依赖树         |
  |     性能     |          极快，无需重新打包整个项目   |         需要loader和plugin处理          |
  |   支持范围   |         原生支持vue/react等           |   需要配置react-refresh或者vue-loader   |
  | css更新内容  |         直接更新，无页面刷新          |            直接更新，无页面刷新         |
  |   支持范围   |       仅替换组件，不影响状态          |  可能会丢失状态（React需react-refresh） |
  |   支持范围   |       模块级更新，不影响页面状态      |     依赖链更新，可能导致整个页面刷新    |
  |   支持范围   |           需要手动重启 Vite           |          需要手动重启 Webpack           |

 ### vite更新示例
  - 1.基于 ES Modules (import) 直接更新模块，不需要重新编译整个项目。
  - 22.利用 **WebSocket** 监听变更，局部更新文件，无需整个页面刷新。
  - 3.对于 CSS / Vue SFC（单文件组件），可以精准替换，不影响页面状态。
  ```js
  // Vite 内部 HMR 机制,直接替换模块，不会触发整个应用重新加载
    import.meta.hot.accept((newModule) => {
      updateComponent(newModule.default)
    })
  ```
  ### webpack更新示例
  - 1.使用 Webpack Dev Server + HMR 插件，监听文件变化。
  - 2.通过 Webpack **module.hot.accept()** 处理模块更新。
  - 3.模块更新时，需要重新构建依赖树，部分依赖可能会影响整个项目。
  ```js
    if (module.hot) {
      module.hot.accept('./App.vue', () => {
        const NewApp = require('./App.vue').default
        app.component('App', NewApp)
      })
    }
  ```
  [!参考文章--Vite和Webpack的HMR有什么区别]https://www.cnblogs.com/LylePark/p/18774403
  [!参考文章--vite热更新原理]https://cloud.tencent.com/developer/article/2414337
