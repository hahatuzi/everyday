# 一： 仅通过react-script包来创建项目
  (1)创建项目目录：
  public--> index.html --> <div id="app"></div>
  src --> App.js --> index.js
  (2)初始化npm i
  (3)安装依赖npm i react react-dom react-scripts -S
  (4)运行npx react-scripts start启动项目或者修改package.json配置文件后运行npm run start
  ```js
    "scripts": {
      "start": "react-scripts start",
    },
  ```
  (5)打包：使用npx react-scripts build打包或者修改package.json打包

  # react全局挂载方法
  ```js
 import message from 'antd'
 React.$message = function (msg) {
  const {type = 'success', content, duration = 1, onclose} = {...arg}
  message[type](content, duration, onclose)
 }

 // 其他页面调用
 import React from 'react'
 export default funtion Index () {
  <Button onClick={() => {
    React.$message({type:'success', content:'成功', duration:2, onclose:() => {console.log('close')}})
  }}></Button>
 }
  ```

  # 56 个 NPM 包解决 16 个 React 问题
  [!链接]https://segmentfault.com/a/1190000040569553
