# Object.prototype.hasOwnProperty()
```js
/*
* 指示对象自身属性中是否具有指定的属性。会忽略掉原型身上继承的属性。
* obj.hasOwnProperty(prop)
* prop:该对象要检测的属性
* return:Boolean
*/
```
# 特殊情况处理
使用 hasOwnProperty 作为属性名
JavaScript 并没有保护 hasOwnProperty 这个属性名，因此，当某个对象可能自有一个占用该属性名的属性时，就需要使用外部的 hasOwnProperty 获得正确的结果：
```js
var obj = {
  hasOwnProperty:function () {
    console.log('自定义hasOwnProperty')
  }
}
// obj.hasOwnProperty实际调用的就是obj自身的方法，而非从原型身上继承的hasOwnProperty方法。
// 所以此时我们可以使用原型链上真正的hasOwnProperty方法。
{}.hasOwnProperty.call(obj)
// 或者Object原型上的hasOwnProperty属性
Object.prototype.hasOwnProperty.call(obj)
```