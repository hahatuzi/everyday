# 谨慎在图片标签上添加点击事件！！！
起因：因为推广落地页的需求需要：所以在图片标签上添加了点击事件，没想到落地页在投放百度APP时出现了图片点击以后直接进入预览状态的bug.
原因：部分安卓机型下的浏览器会存在图片点击以后变成预览模式的问题。如百度APP
解决方法：添加属性：pointer-events：none
pointer-events：指定什么情况下特定的图形元素可以变成鼠标事件。
auto,
none,
inherit,
initial,
unset
# 垂直居中div内的一张img:
```js
div{
    line-height:200px;
    img{
        vertical-align: middle
    }
}
```