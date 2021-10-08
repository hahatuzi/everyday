# document.documentElement和document.body
document.documentElement为文档对象模型的根节点即html标签
document.body为body子节点，即body标签
当存在DTD时，即指定了 DOCTYPE时使用scrollTop时，用document.documentElement.scrollTop 代替 document.body.scrollTop
应用场景：软键盘弹出时fixed定位的元素被顶上去的现象解决方案：
1.获取页面的屏幕高度
2.使用window.resize获取实时屏幕高度，
3.两者比较，进一步处理。
# element元素对象的属性小结：
有哪些属性是可以修改element信息的？
```js
element.className
element.focus()
element.id
element.innerHTML
element.setAttribute
element.style
```