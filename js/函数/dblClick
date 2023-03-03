# 在同一div上同时绑定单击click和双击dblclick事件
**造成的问题**双击时会触发两次单击事件
**解决方法**使用延时器来区别是否为单击事件
```js
// 单击tag
const handleClick = () => {
  if (state.timer) {
    clearTimeout(state.timer)
  }
  // 设置延时器 超过300ms为单击 300ms内点击则为双击事件
  tag.timer = setTimeout(() => {
    // 需要执行的逻辑代码...
  },300)
}
// 双击tag
const handleDbClick = () => {
  if (state.timer) {
    // 清除延时器
    clearTimeout(state.timer)
  }
  // 需要执行的逻辑代码...
}
```