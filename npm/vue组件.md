# vue的插件模式需要暴露一个install模式
```js
Vue.use()
const install = (Vue) => {
  Vue.component(组件.name，组件)
}
export default install
```

# 流程，经过实验，个人将发布组建的过程分为三个步骤
#### 步骤一：注册组件
    ```js
    import tinymce from './tinyMce/index'
    const components = [ tinymce ]
    // 定义 install 方法，接收 Vue 作为参数。如果使用 use 注册插件，则所有的组件都将被注册
    const install = Vue => {
        // 判断是否可以安装
        if (install.installed) return
            // 遍历注册全局组件
        components.forEach(component => Vue.component(component.name, component))
    }
    // 判断是否是直接引入文件
    if (typeof window !== 'undefined' && window.Vue) {
        install(window.Vue)
    }
    export default {
        // 导出的对象必须具有 install，才能被 Vue.use() 方法安装
        install,
        // 以下是具体的组件列表,这样的话就可以单独使用vue.component()来使用某个组件
        tinymce
    }
    ```
#### 步骤二：打包成js文件
    ```js
        "lib": "vue-cli-service build --target lib 要打包的文件路径，即步骤一中install所在的目录 --name 打包后的文件夹名字 --dest 打包后的文件夹名字"
        // 例如
        // "lib": "vue-cli-service build --target lib ./src/packages/index.js --name my-ui --dest my-ui"
    ```
#### 步骤三：npm发布
(1)在我们**打包后的文件夹下**使用命令 **npm init -y**，大白话：使用npm init -y初始化我们打包后的文件夹，生成的pachage.json如下
```js
    {
    "name": "my-ui",
    "version": "1.0.0",
    "description": "",
    "main": "my-ui.common.js",
    "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
    },
    "keywords": [],
    "author": "",
    "license": "ISC"
    }
```
(2)指定npm入口文件为umd.js的所在目录，如"main": "lib/lib.umd.min.js",
(3)npm publish进行发布

# 使用
npm i my-ui
import my-ui from 'my-ui'
import '../node_modules/my-ui/my-ui.css'
Vue.use(my-ui)