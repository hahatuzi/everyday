# HTML拖放API应用
完整的拖放功能包括两部分drag & drop：拖拽和放置。用户选中一个可拖拽元素然后将它拖拽到一个可放置元素内，然后释放鼠标。
### 拖拽过程涉及的事件
事件名     | 介绍
-------- | -----
drag  | 当拖拽元素或选中的文本时触发。
dragend  | 当拖拽操作结束时触发 (比如松开鼠标按键或敲“Esc”键).
dragenter  | 当拖拽元素或选中的文本到一个可释放目标时触发
dragexit  | 当元素变得不再是拖拽操作的选中目标时触发。
dragleave  | 当拖拽元素或选中的文本离开一个可释放目标时触发。
dragover  | 当元素或选中的文本被拖到一个可释放目标上时触发
dragstart  | 当用户开始拖拽一个元素或选中的文本时触发
drop  | 当元素或选中的文本在可释放目标上被释放时触发

**注**在上述事件中有一部分事件会被多次触发：drag和dragover
### 一个简单的拖拽的实现流程：
完整版可以参见[文档](https://developer.mozilla.org/zh-CN/docs/Web/API/HTML_Drag_and_Drop_API)
(1)确定可拖拽对象：
给被拖拽对象添加draggable属性，再添加全局时间处理函数dragstart
(2)定义拖拽数据
dataTransfer属性用来管理拖拽数据，具体为e.dataTransfer.setData('')
(3)定义一个放置区(可释放元素)
默认html元素不会响应拖拽事件，所以我们必须通过添加dragover 和 drop事件来让一个元素变成可释放元素。
```js
<div @drop="handleDrop" @dragOver="handleOver"></div>
handleDrop (e){
  e.preventDefault()
  var data = e.dataTransfer.getData('')
  e.target.appendChild(document.getElementById(data))
}
handleOver (e) {
  e.preventDefault()
}
```