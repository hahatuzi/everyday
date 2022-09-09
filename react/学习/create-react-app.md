# react-script
  react-script是create-react-app的一个核心包，一些脚本和工具的默认配置都集成在里面
# npm run eject
  该操作会复制所有依赖文件和相应的依赖（webpack,babel等）到你的项目，是个单项的操作，一旦eject，npm run eject的操作是不可逆的
  # 全局配置scss
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