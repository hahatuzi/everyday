# 绑定事件处理函数
  - 增加项：新增对应数据---> 渲染列表
  - 删除项：删除对应数据 --> 渲染列表
  - 改变项：改变对应数据 --> 改变列表

# 面向对象处理方式：从外层的浏览器事件到调用方法再到事件处理函数的绑定
  - 操作数据：addToDo, removeToDo, toggleComplete
  - 操作DOM：addItem, removeItem, changeCompleted
  - 管理模板： todoView --> 接收参数