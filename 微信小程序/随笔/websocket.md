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