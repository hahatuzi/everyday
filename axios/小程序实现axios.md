# request.js
  ```js
    function isProtocol(url) {
      return /^(http|https):\/\//.test(url);
    }

    export default class request {
        configure = {
            baseURL: '', // 请求url地址
            url: '', // 完整请求路径url
            header: {
                'content-type': 'application/json'
            }, // header
            method: 'GET', // 请求的类型，支持get，post，put，delete等
            dataType: 'json', // 返回的数据格式，默认json
            responseType: 'text', // 响应的数据格式，默认text
            data: {}, // 传参
            timeout: 3 * 1000, // 请求超时时间
        }

        // 构造器
        constructor(props) {
            this.configure = Object.assign(this.configure, props);
        }

        static create(configure = {}) {
            return new this(configure);
        }

        // 拦截器
        interceptors = {
            request: {
                use: (configCb) => {
                    if (configCb) this.interceptors.request.before = configCb;
                },
                before: configCb => {
                    return configCb;
                }
            },
            response: {
                use: (successCallback, errorCallback) => {
                    if (successCallback) this.interceptors.response.success = successCallback
                    if (errorCallback) this.interceptors.response.error = errorCallback
                },
                success: successCallback => {
                    return successCallback
                },
                error: errorCallback => {
                    return errorCallback
                }
            }
        }

        request(method, url, data, header) {
            this.configure.method = method
            this.configure.url = isProtocol(url) ? url : this.configure.baseURL + url;
            this.configure.data = data,
                this.configure.header = header
            // this.configure.header = Object.assign(this.configure.header, header)
            // 执行请求拦截器
            this.interceptors.request.before({...this.configure})
            return new Promise((resolve, reject) => {
              wx.request({
                  
                    ...this.configure,
                    success: res => {
                        if (res && res.statusCode == 200) {
                            this.interceptors.response.success(res).then(res => {
                                resolve(res)
                            }).catch(error => {
                              if (this.configure.url.endsWith('/system/user/getUser')) {
                                wx.removeStorageSync('GSL_TOKEN')
                              }
                              const emoji = "🙈"
                              console.log(emoji,emoji,emoji,'error','--->', error)
                                wx.showToast({
                                    title: error.msg,
                                    icon: 'none'
                                })
                            })
                        } else {
                            this.interceptors.response.error(res).catch(error => {
                              const emoji = "🙈"
                              console.log(emoji,emoji,emoji,'error','--->', error)
                            })
                        }
                    },
                    fail: error => {
                        this.interceptors.response.error(error).catch(error => {
                            const emoji = "🙈"
                            console.log(emoji,emoji,emoji,'error','--->', error)
                            wx.showToast({
                                title: error.errMsg,
                                icon: 'none'
                            })
                        })
                    }
                })
            })
        }

        get(url, data = {}, header = {}) {
            return this.request('GET', url, data, header)
        }

        post(url, data = {}, header = {}) {
            return this.request('POST', url, data, header)
        }

        put(url, data = {}, header = {}) {
            return this.request('PUT', url, data, header);
        }

        delete(url, data = {}, header = {}) {
            return this.request('DELETE', url, data, header);
        }
    }

  ```

# http.js
  ```js

    import request from './request'
    import Notify from '../miniprogram_npm/@vant/weapp/notify/notify';

    const app = getApp()
    const http = request.create({
        baseURL: app.globalData.baseURL, // 请求后台api的地址，可以抽离出去
    })

    http.interceptors.request.use(config => {
        if (config.header.hasOwnProperty('isToken') && config.header['isToken'] === false) {
            return config;
        }
        let Authorization = wx.getStorageSync('GSL_TOKEN')
        if (Authorization) {
            config.header['Authorization'] = Authorization
        }
        // 每次请求都可以在header中带参数
        return config;
    })

    http.interceptors.response.use(res => {
        if (res.data.code === 200) {
            return Promise.resolve(res.data)
        } else if (res.data.code === 401) {
            wx.reLaunch({
                url: '/pages/login/login',
            })
            wx.removeStorageSync('GSL_TOKEN')
            return Promise.reject(res.data)
        } else {
            return Promise.reject(res.data)
        }
    }, error => {
        return Promise.reject(error)
    })
    export default http

  ```

# api
  ```js
    import http from '../utils/http.js'

    export const login = params => http.post('/login', params, {isToken: false})
    export const loginByWeixin = params => http.post('/system/user/login_by_weixin', params)
    export const getNameCount = name => http.get(`/countByNickName/${name}`)
  ```

