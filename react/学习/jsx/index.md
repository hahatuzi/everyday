# jsx语法规范
（1）使用{}插入表达式
（2）style中必须使用对象
# className和style多个
```js
<div className={styles.child + ' ' + (item.show ? styles.child_select : '')}></div>
<div className={["title", index === this.state.active?"active":null].join(' ')}></div>
```