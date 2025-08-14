# 1.router.addRoute和addRoutes的区别
```js
router.addRoutes(newRoutes)
for(let item of newRoutes) {
  router.addRoute(item)
}
```

# 路由生命周期
->导航被触发
-->触发失活组件的beforeRouteLeave
-->调用全局的beforeEach守卫
-->如果是重新加载复用组件处罚beforeRouteUpdate
-->如果组件内有单独守卫beforeEnter,则触发
-->解析异步路由组件
-->触发被激活组件的beforeRouteEnter
-->触发全局的beforeResolve
-->导航被确认
-->触发全局的afterEach
-->触发dom更新
-->调用beforeRouteEnter的next方法，并将组件作为参数传递进去