```js
function render(vDom, container) {
  let dom
  if (typeof vDom === 'object') {
    dom = document.createTextNode(vDom)
  } else {
    dom = document.createElement(vDom.type)
  }
  // 将vDom上传了children外的属性都挂在到真正的DOM上
  if (vDom.props) {
    Object.keys(vDom.props)
          .filter(key => key != 'children')
          .forEach(item => dom[item] = vDom.props[item])
  }

  // 如果还有子元素，递归调用
  if (vDom.props && vDom.props.children && vDom.props.children.length) {
    vDom.props.children.forEach(child => render(child, dom))
  }

  container.appendChild(dom)
}

// requestIdleCallback
// window.requestIdleCallback(callback, options)
// callback回调函数将会在浏览器空闲的时候呗调用，不会影响延迟关键时间，比如动画和输入响应。
```
