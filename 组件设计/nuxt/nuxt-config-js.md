# nuxt.config.js文件解析
router属性解析
```js
router:{
  // 中间件
  middleware:'auth',
  // 扩展路由
  extendRouters (routers,resolve) {
    // 其中涉及路由参数校验，在组件路由中使用服务端钩子函数validate({}){
    //   return
    // }
    routers.push({
      name:'home',
      path: 'index',
      component: resolve(__dirname, 'pages/index.vue)
    })
  }
}

```