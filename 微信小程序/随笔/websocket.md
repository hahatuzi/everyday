# 一：websocket基本方法
### 1.wx.connectWebsocket
### 2.wx.onSocketOpen
(1)原本以为connectWebsocket.success和onSocketOpen的实际使用性质一样，都属于监听是否连接成功，后来发现connectWebsocket.success是监听是否传递了url，header等参数，并未真正开始建立连接。而onSocketOpen实际上监听的则是传递的url是否正确，服务是否能连接成功，websocket是否建立成功。
(2)原本以为onSocketError和onSocketClose不管写在哪里都可以，不论是和connectWebsocket同级还是写在connectWebsocket.success的回调函数内。毕竟实际上无论写在上述哪个成精都可以触发。但理清connectWebsocket.success和onSocketOpen的区别后发现，还是写在connectWebsocket.success的回调函数内符合实际逻辑！！！
url错误  --> connectWebsocket.success --> 与connectWebsocket同级的onSocketError  --> 与connectWebsocket同级的onSocketClose
```js
 wx.connectSocket({
        url: 'localhost:8080',
        header: {'content-type': 'application/json'},
        success: function () {
          console.log('websocket连接成功~')// 可以理解为此时开始建立webSocket连接，但未开始检验url和header参数的正确性！！
          wx.onSocketOpen(function (res) {
            console.log(res, '连接建立成功,url,header等参数也无任何错误')
      
              //接受服务器消息
              wx.onSocketMessage(func);//func回调可以拿到服务器返回的数据
          });
          wx.onSocketError(function (res) {
            console.log(res, '连接出现错误，比如url拼接错误')
            console.log(res)
            wx.showToast({
                title: '111',
                icon: "none",
                duration: 2000
            })
          })
          // 当SocketError时会触发SocketClose
          wx.onSocketClose((result) => {
            console.log('websocket关闭')
          })
        },
        // 经过实践发现只有当url或者header缺失时会触发fail，如果url路径拼接错误并不会触发fail
        fail: function (res) {
          console.log('websocket连接失败~')
        }
    })
```
### 3. wx.onSocketMessage(func);//func回调可以拿到服务器返回的数据
# 二：websockst的封装：
包括建立连接，监听消息，发送消息，心跳检查，断线重连等功能
心跳和检查的目的：一句话概括就是客户端和服务器端彼此确认对方是否还活着，避免丢包发生。
心跳检查的操作，通过在指定时间间隔发送心跳包来确定是否连接正常，如果出现问题就手动触发oncolse方法，并且重新连接reconnect
websocket断开的情形：
(1)客户端断开
通常是因为网络问题导致websocket断开。，当然hiah可能因为浏览器自身的特性导致触发onclose的时机不同问题，引起不能理想执行onclose方法，促使我们无法知道是否断开连接的情况发生。
（2）服务端断开，如果情况可控，客户端能够通过onclose知道服务断开。但是如果情况不可控制，我们几需要通过心跳检查来判断。

# 三：流程图：
创建websocket链接对象 --> 连接失败 -->  是否为客户端主动断开连接   -->  否 -->  reconnect
                                                                   -->  是 -->  删除所有心跳
                      --> 连接成功 -->  添加心跳  -->  发送ping -->  服务器是否响应  -->  是 -->   连接正常  -->  清除上一个心跳的饿定时器记录，并重新添加心跳
                                                                                     -->  否 -->   连接失败  -->  reconnect
添加心跳解释：（一段时间后发送ping给服务器，同时做好服务器已经断开连接的准备：添加尝试重新连接的定时器）



```js
let timeoutObj = ''
let serverTimeoutObj = ''
// 开始心跳
function reset() {
  clearTimeout(this.timeoutObj)
  clearTimeout(this.serverTimeoutObj)
}
function start() {
  var num = 10
  this.timeoutObj = setTimeout(() => {
    console.log('发送心跳')
    wx.sendSocketMessage({
      data: msg,
      success: (res) => {
          console.log('心跳发送成功') // 表示能正常连接，并能成功发送消息
      },
      fail: (error) => {
          console.log(error)
          wx.showToast({
              title: '消息发送异常',
              icon: "none",
              duration: 2000
          })
      }
  });
  }, 5 * 1000)
}
function connect(user, toUserId, func) {
  wx.connectSocket({
    url: 'localhost:8080',
    header: {'content-type': 'application/json'},
    success: function () {
      console.log('websocket连接成功~')// 可以理解为此时开始建立webSocket连接，但未开始检验url和header参数的正确性！！
      wx.onSocketOpen(function (res) {
        console.log(res, '连接建立成功,url,header等参数也无任何错误')
        //接受服务器消息
        wx.onSocketMessage(res => {
          if (res.type == 'pong') {
            this.reset()
            this.start()
          } else {
            func()
          }
        });//func回调可以拿到服务器返回的数据
      });
      wx.onSocketError(function (res) {
        console.log(res, '连接出现错误，比如url拼接错误')
        console.log(res)
        wx.showToast({
            title: '111',
            icon: "none",
            duration: 2000
        })
      })
      // 当SocketError时会触发SocketClose
      wx.onSocketClose((result) => {
        console.log('websocket关闭')
      })
    },
    // 经过实践发现只有当url或者header缺失时会触发fail，如果url路径拼接错误并不会触发fail
    fail: function (res) {
      console.log('websocket连接失败~')
    }
  })
}

//发送消息
function send(msg) {
  wx.sendSocketMessage({
      data: msg,
      success: (res) => {
          console.log(res)
      },
      fail: (error) => {
          console.log(error)
          wx.showToast({
              title: '消息发送异常',
              icon: "none",
              duration: 2000
          })
      }
  });
}
```