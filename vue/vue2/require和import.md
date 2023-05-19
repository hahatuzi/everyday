# import和import()和reqiure()的区别
（1）首先require()是AMD规范下的语法。import和import()是es6语法，其中import()是ES2020的语法
（2）import是**静态加载**，import()和require()是**动态按需加载**
import()函数则是动态按需加载**返回Promise 对象**。import()函数可以用在任何地方，不仅仅是模块，非模块的脚本也可以使用。
import()函数它是运行时执行，也就是说，什么时候运行到这一句，就会加载指定的模块。
import()函数与所加载的模块没有静态连接关系，这点也是与import语句不相同。import()类似于 Node 的require方法，区别主要是前者是**异步加载**，后者是**同步加载**。
```js
// import()的使用如下
import('moduleA').then()
```
[!参考链接]https://www.zhihu.com/question/56820346