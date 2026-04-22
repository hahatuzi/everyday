# render阶段
  > 流程：performConcurrentWorkOnRoot --> renderRootSync --> workLoopSync --> performUnitOfWork --> beginWork --> completeUnitOfWork --> completeWork
  performConcurrentWorkOnRoot这个函数中有两个重要的阶段：render和commit
  ### 1.render阶段的过程
   - (1)executionContext |= RenderContext
   - (2)workInProgressTransitions赋值getTransitionForLane(root,lanes)
   - (3)**prepareFreshStack**初始化
   - (4)workLoopSync，**从根节点开始遍历Fiber树**，perfromUnitOfWork(beginWork更新当前fiber,比如props,state更新，生命周期函数执行，hooks函数执行等，返回下一个fiber, complateUnitOfWork)
   - (5)workInProgressX,workInProgress已经在preformUnitWork阶段更新
   - (6)再遍历一遍更新队列，finishQueueingConcurrentUpdates()
  ### beginWork
  beginWork --> reconcileChildren --> createChildReconciler

  ### renderRootConcurrent

  ### completeWork
  commitMutationEffects --> commitMutationEffectsOnFiber --> 


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
