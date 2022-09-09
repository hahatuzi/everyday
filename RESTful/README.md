# axios:它依赖于ES6的语法promsie，如果你的环境不支持ES6 promise，那么你就需要使用polyfill。安卓 4.x
# axios特点
1。.基于promise请求
2.支持请求取消
3.包括请求拦截器和相应拦截器
4.支持浏览器和node
5.请求和响应数据支持数据类型转化
6.可以批量发送多个请求
# axios常用语法
axios.create([config])创建一个新的axios实例对象


axios.cancel()用于创建取消请求的错误对象
axios.cancelToken()用于创建取消请求的token对象
axios.isCancel()是否是一个取消请求的错误
axios.all(promises对象)用于批量执行多个异步请求\

# axios的请求拦截器
axios.interceptors.request.use(请求成功回调函数，请求失败回调函数)
```js
axios.interceptors.request.use(
  config =>{
    console.log('请求拦截器1')
    return config
  },
  error =>{
    return Promise.reject(error)
  }
)
axios.interceptors.response.use(
  reponse =>{
    console.log('响应拦截器1')
    return reponse
  },
  error =>{
    return Promise.reject(error)
  }
)

axios.interceptors.request.use(
  config =>{
    console.log('请求拦截器2')
    return config
  },
  error =>{
    return Promise.reject(error)
  }
)
axios.interceptors.response.use(
  reponse =>{
    console.log('响应拦截器2')
    return reponse
  },
  error =>{
    return Promise.reject(error)
  }
)
```
# 当有多个成对的请求拦截器和响应拦截器时