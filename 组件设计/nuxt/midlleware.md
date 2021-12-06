# middleware文件夹解析
```js
export default ({store, route, redirect, params, query, req, res}) => {
    // context 服务端上下文
    // store 状态树信息
    // route 一条目标路由信息
    // redirect 强制跳转
    // parmas, query校验参数合理性
    // 全局路由守卫前置， (1)依赖插件(2)nuxt-config-js文件夹下的route中的middleware配置指向配置。
    redirect('/')
}
```