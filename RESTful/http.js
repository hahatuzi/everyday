import axios form 'axios'
// switch 
axios.defaults.timeout = 10000
axios.defaults.withCredentials = true
// 指定请求数据的格式
axios.post(url,data)
axios,defaults.header['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.transformRequest = data => qs.stringify(data)
// 设置请求拦截器,添加token校验(JWT校验),存储到vuex或者本地存储中，并且在每一次服务器请求数据时都要带上token
axios.interceptors.request.use(() => {
  let token = localStorage.getItem('token')
  token && config.headers.Authorization = token
  return config
},error => { return Promise.reject(error) })

//响应拦截器
axios.interceptors.response.use(response => {
  // 自定义响应成功的http的状态码
  return response.data
}, error => {
  let {response} = error
  if (response) {
    // 服务器起码返回数据了
    switch (response.status){
      case 401: // 权限问题，未登录
        break;
      case 403: // 服务器拒绝执行，token过期
      case ...
    }
  } else {
    // 服务器连结果都没有返回
    if (!window.navigator.onLine) {
      // 客户端断网处理，可以跳转到断网页面
      return
    }
    return Promise.reject(error)
  }
})