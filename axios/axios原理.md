# 拦截器原理
  ```js
    function Axios() {
      this.interceptors = {
        //两个拦截器
        request: new interceptorsManner(),
        response: new interceptorsManner()
      }
    }

    //真正的请求
    Axios.prototype.request = function () {
      let chain = [dispatchRequest, undefined] //这儿的undefined是为了补位，因为拦截器的返回有两个
      let promise = Promise.resolve()
      //将两个拦截器中的回调加入到chain数组中
      this.interceptors.request.handler.forEach((interceptor) => {
        chain.unshift(interceptor.fulfilled, interceptor.rejected)
      })
      this.interceptors.response.handler.forEach((interceptor) => {
        chain.push(interceptor.fulfilled, interceptor.rejected)
      })
      while (chain.length) {
        //promise.then的链式调用，下一个then中的chain为上一个中的返回值，每次会减去两个
        //这样就实现了在请求的时候，先去调用请求拦截器的内容，再去请求接口，返回之后再去执行响应拦截器的内容
        promise = promise.then(chain.shift(), chain.shift())
      }
    }

    function interceptorsManner() {
      this.handler = []
    }

    interceptorsManner.prototype.use = function (fulfilled, rejected) {
      //将成功与失败的回调push到handler中
      this.handler.push({
        fulfilled: fulfilled,
        rejected: rejected
      })
    }

    //类似方法批量注册,实现多种请求
    util.forEach(['get', 'post', 'delete'], (methods) => {
      Axios.prototype[methods] = function (url, config) {
        return this.request(
          util.merge(config || {}, {
            //合并
            method: methods,
            url: url
          })
        )
      }
    })

  ```