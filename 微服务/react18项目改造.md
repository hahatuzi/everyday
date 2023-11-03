# 第一步：改造入口文件index.js
  ```js
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import {HashRouter} from 'react-router-dom'
  import './index.css';
  import App from './App';
  import reportWebVitals from './reportWebVitals';
  import './public-path.js'

  let root 
  let publicPath // 路由公共前缀从主应用中获取
  // 将render方法用函数包裹，以供后续主应用和自应用独立运行
  function render (props) {
    const {container} = props
    const dom = container ? container.querySelector('#root') : document.getElementById('root')
    root = ReactDOM.createRoot(dom)
    root.render(
      // basename匹配的是activeRule
      <HashRouter basename={window.__POWERED_BY_QIANKUN__ ? publicPath : ''}>
        <React.StrictMode>
          <App />
      </React.StrictMode>
      </HashRouter>
    );
  }

  // 判断是否在qiankun环境下，非qiankun环境在独立运行
  if (!window.__POWERED_BY_QIANKUN__) {
    render({})
  }
  // 各生命周期
  // bootstrap只会在自应用初始化的时候调用一次！！！下次自应用进入时会直接调用mount狗子
  export async function bootstrap () {
    console.log('bootstrap')
  }
  export async function mount (props) {
    console.log('sub_react mount',props)
    publicPath = props.publicPath
    render(props)
  }
  export async function unmount (props) {
    console.log(props)
    root.unmount()
    root = null
  }
  reportWebVitals();
  ```

# 第二步：新增public-path.js文件
  ```js
  if (window.__POWERED_BY_QIANKUN__){
    // 动态设置webpack publicPath，防止资源加载出错
    // eslint-disable-next-line no-undef
    __webpack_public_path__ = window.__INJECTED_PUBLIC_PATH_BY_QIANKUN__
  } // 用于展示图片等路径展示不出来的问题
  ```
# 第三步：为了不eject所有的配置，我们选择用react-app-rewires工具来改造webpack配置，安装react-app-rewired插件
  ```js
  // npm i react-app-rewired
  // 修改package.json中的scripts
    "scripts": {
      "start": "react-app-rewired start",
      "build": "react-app-rewired build",
      "test": "react-app-rewired test",
      "eject": "react-app-rewired eject"
    },
  ```
# 第四步：修改webpack配置文件，在根目录下新增config-overrides.js文件
  ```js
  // 将项目打包成umd模块，方便qiankun读取暴露出来的生命周期
  const {name} = require('./package');
  module.exports = {
    webpack: (config) => {
      config.output.library = `${name}-[name]`;
      config.output.libraryTarget = 'umd';
      config.output.chunkLoadingGlobal = `webpackJsonp_${name}`;
      return config
    }
  }
  ```