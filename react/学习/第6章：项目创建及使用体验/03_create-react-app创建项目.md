create-react-app底层由webpack构建
# 一：创建过程
  ### 第一步： npx create-react-app 项目名 --template typescript，来创建项目
  ### （2）npm i
  ### (3)npm i react-router-dom
  ### (4)npm run start
# npm run eject
  该操作会复制所有依赖文件和相应的依赖（webpack,babel等）到你的项目，是个单项的操作，一旦eject，npm run eject的操作是不可逆的
  ### （3）全局配置scss
  -----------------------------------
  在不使用npm run eject暴露配置的情况下

  1. 安装 node-sass sass-resources-loader
  ```js
  npm install node-sass sass-resources-loader --save
  ```
  2. 安装 react-app-rewired（重写react脚手架配置）和 customize-cra（帮助你自定义react脚手架配置）
  ```js

  npm install react-app-rewired customize-cra --save
  ```
  3. 在项目根路径下新建一个js文件  config-overresides.js
  ```js
  const { override, adjustStyleLoaders}  = require("customize-cra");
  module.exports = override(
      adjustStyleLoaders(rule => {
          if (rule.test.toString().includes('scss')) {
              rule.use.push({
                  loader: require.resolve('sass-resources-loader'),
                  options: {
                      resources: [
                          './src/assets/_vars.scss'
                      ]
                  }
              });
          }
      })
  );
  ```
  4. 修改 package.json
  ```js

    "scripts": {
      "start": "react-app-rewired start",
      "build": "react-app-rewired build",
      "test": "react-app-rewired test",
      "eject": "react-app-rewired eject"
    },
  ```
  配置之后重启项目即可。
  -----------------------------------
# 二：操作及概念解读
  ### （1）react-script
  react-script是create-react-app的一个核心包，一些脚本和工具的默认配置都集成在里面
# 三：项目结构解读
  ### (1)reportWebVitals.js文件
  webvital用来监测用户体验程度，其中包含了几个指标
  LCP：最大用户渲染时间
  FID：首次输入延时
  CLS:累计布局偏移
  FCP:首次绘制时间
  TTIB：首字节到达时间
  ```js
  // 可以通过以下代码来查看详细信息
  reportWebVitals(console.warn);

  ```
  [!参考链接]https://blog.csdn.net/qiuqiu1894/article/details/123976582
  ### (2)React.Fragment
  是一个专门用来作为父容器的组件，它会将其中的资源塑直接返回，不会创建多余的父元素

# 四：代理http-proxy-middleware

