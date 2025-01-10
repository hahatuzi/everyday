#　一.axios和Axios的关系：
  - （1）语法上来说，axios不是Axios的实例,因为Axios是一个函数
  - （2）从功能上来说axios是Axios的实例
  - （3）axios是Axios.prototype.request函数bind()返回的函数
  - （4）axios作为对象，它身上有Axios原型对象上的所有方法，及Axios对象的所有属性
  ```js
    --> axios -->  axios = function createInstance(defaults) {return instance}  -->  instance  -->  instance = bind(Axios.prototype.request, new Axios(defaults))
    
    function Axios () {}
    Axios.prototype.request = function () {
      return promise
    }

    function createInstance (defaults) {
      let context = new Axios(defaults)
      let instance
      instance = bind(Axios.prototype.request, context) // Axios.prototype.request.bind(context)
      // 工厂函数，返回值为
      instance.create = function create(instanceConfig) {
        return createInstance(mergeConfig(defaultConfig, instanceConfig));
      };
      return instance
    }

    let axios = createInstance(defaults)
    // axios和axios.create()对应的就是request函数
    axios.Axios = Axios;
    axios.CanceledError = require('./cancel/CanceledError');
    axios.CancelToken = require('./cancel/CancelToken');
    axios.isCancel = require('./cancel/isCancel');

    // axios.create  -->  instance.create  -->  createInstance() {} -->  instance
  ```

# 二：instance和axios的区别
  - 1.相同点
    （1）都是一个能发任意请求的函数，request(config)
    （2）都有分特定请求的各种发，get/post/put/delet
    （3）都有默认配置和拦截器属性defaults/interceptors
  - 2.不同点
    （1）默认匹配的值很可能不一样
    （2）instancec没有axios后面添加的一些方法，create()/cancelToken()/all()

# 三：axios的运行整体流程
  
      axios      --> createInstance() --> instance --> Axios.prototpe.request --> 处理请求参数，然后dispatchRequest --> adapter --> 报错cancel --> response interceports  
  axios.create() --> createInstance() --> instance --> Axios.prototpe.request --> 处理请求参数，然后dispatchRequest --> adapter --> 报错cancel --> response interceports

  axios/axios.create()  ----Create an instance of Axios---> createInstance()  ---Create the default instance to be exported--->  执行、别名执行axios()/axios.get()
---->  Axios.protoytpe.request()  --->  request interceptors  --->  dispatchRequest()  ---> adapter()  --->  response interceptors  ---> 请求的onResolved/onRejected
**request(config)**
将请求拦截器、dispatchRequest()、响应拦截器通过promise链串联起来，返回promise
**dispatchRequest(config)**
转换请求数据 --> 调用xhrAdapter()发送请求 --> 请求返回后转换响应数据，返回promise
**xhrAdapter(config)**
创建XHR对象，根据config进行相应设置，发送特定请求，bong接受响应数据，返回promise


# ２.axios.create()
axios.create()的存在原因，因为axios()就可以完成一个请求，那么为什么还需要axios.create()来发送请求呢？
答：目的在于区分多个不同baseUrl下的请求。

# 四.如何取消一个请求
  ### (1)取消请求的场景一：在发送请求后点击按钮来取消请求
  ### (2)取消请求的场景二：在连续发送多次请求时，取消前面的请求
  请求的配置对象中添加cancel属性，该属性会暴露一个取消的回调函数，可以在外部直接使用该函数来取消请求，同时在调用该函数时传递的参数会存在于请求error回调函数中。
  1.当配置了cancelToken对象时
  （1）创建一个用于未来取消请求的cancelPromise
  （2）并定义一个用于取消请求的cancel函数
  （3）将cancel函数传递出来
  2.调用cancel()取消请求
  （1）执行cancel函数，传入错误信息message
  （2）内部会让 cancelPromise变为成功，且成功的值为一个cancel对象
  （3）在cancelPromise的成功回调中中断请求，并让发请求的promise失败，失败的reason为cancel对象
  ```js
    ƒ cancel(message) {
      if (token.reason) {
        // Cancellation has already been requested
        return;
      }

      token.reason = new Cancel(message);
      resolvePromise(token.reason);
    } 
  ```

var context = new Axios()
var instance = bind(Axios.prototype.request,context)
// 将Axios原型对象上的方法拷贝到instance上
utils.extend(instance,Axios.prototype,context)
utils.extend(instance, context)


# 五：源码分析流程：
  - 第一步：从使用时入手：判断axios类型：既可以作为对象也可以作为函数使用
  - 第二步：从使用时入手：判断axios作为函数调用时的返回值类型：Promise类型
  - 第三步：判断axios作为对象时，有哪些属性：get.post.create,
    ```js
      axios({url:'',methods:'get'})
      axios.get({url:''})
      axios.create()
      // 一：如何作为函数使用
      // 所以我们的问题关键就在于构造函数的实例对象如何作为函数来调用构造函数上的方法，需要用到函数身上的bind属性来返回一个函数
      axios() --> instance() -->  Axios.prototype.request.bind(context)()  <-- context = new Axios()

      // 一：如何作为对象使用
      // 将Axios.prototype身上的属性全部拷贝到instance身上
      utils.extend(instance,Axios.prototype)
    ```

# 六：拦截器执行流程分析
  axios拦截器的运行流程，**请求拦截器先添加后执行，响应拦截器后添加先执行**
  ```js
    // 第一步：添加请求拦截器数组和响应拦截器数组
    // requestInterceptorChain.unshift(interceptor.fulfilled, interceptor.rejected)
    var requestInterceptor = [{fulfilled2(){}, reject2(){}}, {fulfilled1(){}, reject1(){}}]
    // responseInterceptorChain.push(interceptor.fulfilled, interceptor.rejected);
    var responseInterceptors = [{fulfilled11(){}, reject11(){}}, {fulfilled22(){}, reject22(){}}]
    var chain = [
      fulfilled2, reject2, fulfilled1, reject1,
      dispatchRequest, undefined,
      fulfilled11, reject11, fulfilled22, reject22
    ]

    //promise链回调：config
                     => (fulfilled2, reject2) => (fulfilled2, reject2) //请求拦截器处理
                     => (dispatchRequest, undefined) // 发请求
                     => (fulfilled1, reject1) => (fulfilled1, reject1) //请求拦截器处理
                     => (onResolved, onRejected) // axios请求回调处理
    // 第二步：将请求拦截器中的元素取出并执行
    try {
      newConfig = onFulfilled(newConfig);
    } catch (error) {
      onRejected(error);
      break;
    }
    // 第三步，执行dispatchRequest
    try {
      promise = dispatchRequest(newConfig);
    } catch (error) {
      return Promise.reject(error);
    }
    // 第四步，使用第三步返回的promise.then来执行响应拦截器
    while (responseInterceptorChain.length) {
      promise = promise.then(responseInterceptorChain.shift(), responseInterceptorChain.shift());
    }
  ```

