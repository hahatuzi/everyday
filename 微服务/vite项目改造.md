# 1.安装vite-plugin-qiankun依赖包
# 2.修改config.js
```js
import qiankun from 'qiankun'
defineConfig({
  base:'/sub-vue', // 和基座中配饰的activeRlue一致
  plugins:[
    vue(),
    qiankun('sub-vue',{

    })
  ]
})
```
# 3.修改main.js文件
```js
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { renderWithQiankun, qiankunWindow } from "vite-plugin-qiankun/dist/helper";

let app
if (!qiankunWindow.__POWERED_BY_QIANKUN__){
  createApp(App).mount('#app')
} else {
  renderWithQiankun({
    mount(props) {
      app = createApp(App)
      app.mount(props.container.querySelector('#app'))
    },
    bootstrap(){
      console.log('vue app bootstrap')
    },
    update () {
      console.log('vue app update');
    },
    unmount(){
      console.log('vue app unmount')
      app?.unmount()
    }
  })
}
```



**附：创建vite项目的步骤**
```js
// 1. npm install vue@latest //创建vue项目
```