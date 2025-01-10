axios:它依赖于ES6的语法promsie，如果你的环境不支持ES6 promise，那么你就需要使用polyfill。安卓 4.x

# 一：axios特点
  - 1.基于**promiseAPI**
  - 2.支持请求取消
  - 3.拦截请求和响应
  - 4.支持浏览器和node发送请求，因为axios的default.js会判断环境，从而使用对应的适配器。从**浏览器**中创建**XMLHttpRequests**,从**node.js**创建**http请求**
  - 5.支持请求和响应数据数据类型转化
  - 6.可以批量发送多个请求
  - 7.自动转换JSON数据
  - 8.客户端支持防御XSPF
  [!参考axios的API]https://www.javasoho.com/axios/index.html#%E7%89%B9%E6%80%A7
# 二：axios常用语法
  - 1.axios.defaults.XXX: 请求的默认全局配置
  - 2.axios.interceptors.request.use()  请求拦截器
  - 3.axios.interceptors.response.use()  响应拦截器
  - 4.axios.create([config])创建一个新的axios实例对象
    ```js
      axios.defaults.headers['Content-Type'] = 'application/json;charset=utf-8'
      const service = axios.create({
        // axios中请求配置有baseURL选项，表示请求URL公共部分
        baseURL: import.meta.env.VITE_APP_BASE_URL + import.meta.env.VITE_APP_BASE_API,
        cancelToken:source.token,
        // 超时
        timeout: 20000
      })
   ```
  - 5.axios.cancel()用于创建取消请求的错误对象
  - 6.axios.cancelToken()用于创建取消请求的token对象
  - 7.axios.isCancel()是否是一个取消请求的错误
  - 8.axios.all(promises对象)用于批量执行多个异步请求\

# 三：axios的请求拦截器
  ```js
    // axios.interceptors.request.use(请求成功回调函数，请求失败回调函数)
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
    //请求拦截器1,请求拦截器2 -->  响应拦截器1,响应拦截器2
  ```
  ### 当有多个成对的请求拦截器和响应拦截器时

# 三：axios请求配置对象config参数汇总：
  ### 1.url:''
  ### 2.baseUrl:'' //将自动添加到url参数的前面
  ### 3.data:{}
    ```js
    // 是作为请求主体被发送的数据
    // 和transformRequest一样仅适用于put,post,和patch
    // 在没有设置 `transformRequest` 时，必须是以下类型之一：
      // - string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
      // - 浏览器专属：FormData, File, Blob
      // - Node 专属： Stream
      // ♡⸜(˶˃ ᵕ ˂˶)⸝♡
    ```
  ### 4.params:{}  // 是即将与请求一起被发送的URL参数
  ### 5.paramsSerializer:function (params) {}
    ```js
      function (params) {
        // 是一个负责将params属性传递的URL参数序列化的函数，
        // 使用场景，比如你在发送get请求时需要将一个数组传递给后端
        // QS.stringify()函数中的第二个参数的含义参见https://www.npmjs.com/package/qs
        return Qs.stringify(params,{arrayFormat:'brackets'})
      }
      // 应用实例
      // 　let params = { id: [1, 2, 3] }
      //    axios.get('www.baidu.com', params); 
      // www.baidu.com?id=1&id=2&id=3
      // 注：虽然parmas属性传递的是URL参数，看起来一般只会在get请求方式下使用，但是为了防止某个post请求或者其他请求有在URL上拼接参数的需要，我们还是尽量避免直接在paramsSerializer属性中处理parmas请求参数，而是改成在请求拦截器中做请求方式判断，若为get请求或者其他有需要的请求方式时再对params参数做处理。
      axios.interceptors.request.use(async (config) => {
        // 只针对get方式进行序列化
        if (config.method === 'get') {
          config.paramsSerializer = function(params) {
            return qs.stringify(params, { arrayFormat: 'brackets' })
          }
        }
      })
    ```
  ### 6.methods:''，axios常见的请求方式：get,post,put,delete
  ### 7.headers:{},
  ### 8.timeout:0
  ### 9.transformRequest:[function (data) { return data }]
    ```js
      // 允许在向服务器发送前修改请求数据,
      // 只能用于put,post,patch这几种请求方法
      // 后面数组中的函数必须返回一个字符串，或者ArrayBuffer,或者Stream
      // 注：使用场景，单次或者少量数据需要处理的时候没必要放在intercptor中处理。
    ```
  ### 10.transformReasponse:[function (data) { return data }]
    ```js
      // 允许在传递给then/catch之前修改响应数据
    ```
  ### 11.withCredentials:false // 表示跨域请求时是否需要使用凭证，默认为false
  ### 12.adapter: function (config){} // 常用于测试时自定义处理请求
  ### 13.auth:{}
  ### 14.responseType:'json' // 服务器响应的数据类型
  ### 15.xsrfCookieName:'XSRF-Token'  // 用作xsrf token的值的cookie的名称
  ### 16.xsrfHeaderName: 'X-XSRF-TOKEN'
  ### 17.cancelToken: new CancelToken(function (cancel) {})
  ### 18.// `validateStatus` 定义对于给定的HTTP 响应状态码是 resolve 或 reject  promise 。如果 `validateStatus` 返回 `true` (或者设置为 `null` 或 `undefined`)，promise 将被 resolve; 否则，promise 将被 rejecte
    validateStatus: function (status) {
      return status >= 200 && status < 300; // 默认的
    },

  ### 19.用于取消请求的cancelToken
    ```js
      // c是用于取消当前请求的函数
      cancelToken: new axios.CancelToken((c) => {
        cancel = c  // 保存取消请求的函数，方便之后想要取消请求时使用
      })
    ```

# 四：取消请求：使用cancelToken取消请求
  ### 场景一：单个请求的取消，比某页面A的请求数据量太大，切换至页面B时取消页面A的请求
    ```js
      let cancel //用于保存取消请求的函数
      function getPro1(params) {
        axios({
          url:'http://localhost:3000/product1',
          cancelToken: new axios.CancelToken(c=> {
            // 保存取消请求的函数，方便之后想要取消请求时使用
            cancel = c
          })
        }).then(res=>{
          console.log('请求1发送成功',res.data)
          cancel = null // 请求结束后就没必要再保存取消请求的函数。通俗来讲就是请求结束后就没办法再取消了
        },error=>{
          console.log('请求失败或者请求取消了',error.message)
          cancel = null
        })
      }
      function cancelReq (params) {
        // 确认是否是在请求发送后的点击取消请求按钮，避免直接点击取消按钮的情况
        if(typeof cancel === 'function') cancel('请求取消')
      }
      onBeforeUnmount(() => {
        cancelReq()
      })
    ```

  ### 场景二：多次连续点击请求时取消前面的请求
    ```js
      let cancel //用于保存取消请求的函数
      function getPro1(params) {
        if (typeof cancel === 'function') {
          cancel('取消请求')
        }
        axios({
          url:'http://localhost:3000/product1',
          cancelToken: new axios.CancelToken(c=> {
            // 保存取消请求的函数，方便之后想要取消请求时使用
            cancel = c
          })
        }).then(res=>{
          console.log('请求1发送成功',res.data)
          cancel = null // 请求结束后就没必要再保存取消请求的函数。通俗来讲就是请求结束后就没办法再取消了
        },error=>{
          // 此处要区分到底时请求失败了还是请求取消了
          if (axios.isCancel(error)) {
            console.log('请求1取消了',error.message)
          } else {
            console.log('请求1失败',error.message)
            cancel = null
          }
        })
      }
    ```

# 3.axios请求创建方式
（1）axios(config)
(2)区分请求方式method的别名请求法
axios.get(url,config对象)
axios.delete(url,config对象)
axios.post(url,data对象,config对象)
axios.put(url,data对象,config对象)
axios.patch(url,data对象,config对象)
**注：单独将url和data写出来的意思即为不需要在config配置中指定**
```js
axios.get('/user',{baseUrl:'https://localhost:3000',params:{name:'lisa'}})
axios.post('/user',{name:'lisa'},{baseUrl:'https://localhost:3000'})
```