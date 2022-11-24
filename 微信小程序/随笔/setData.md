# setData的修改类型
```js
this.setData({'obj.name': 'lisa'})
this.setData({['obj.name']: 'lisa'})
let key = name; this.setData({['obj.'] + key: 'lisa'})
this.setData({'arrs[1].name': 'lisa'})
this.setData({['arrs[1].name']: 'lisa'})
// 有变量的时候需要拼接字符串，然后再外层加上中括号[]
this.setData({['arrs[' + index + '].name']: 'lisa'})
```