# rrweb插件的操作步骤：
  bug --> 操作数据发送给回访服务 --> 拉取回访数据查看回放

```js
  axois.get('http://localhost:3000/logDetail?logName=' + name),then(res => {
    const {event,error} = JSON.parse(res.data.content)

    document.getElementById('replayer').innerHTML = ''
    const replayer = new Replayer(event, {
      root:document.getElementById('replayer'),
      liveMode: false
    })
    replayer.play()
  })
```