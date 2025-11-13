# 1.jsx语法规范
   - 使用{}插入表达式
   - style中必须使用对象
# 2.变量绑定
# 3.列表绑定
# 4.事件绑定
  ```js
    export function App: JSX.Element(){
      return (
        <div>
          <button onClick={(e: MouseEvent<HTMLButtonElement>) => console.log(e.target)}>click</button>
        </div>
      )
    }
  ```
# 4.jsx实现复杂条件渲染
  ```js
    function getItem () {
      if (state = 1) {
        return <div>1</div>
      } else if (state = 2) {
        return <div>2</div>
      } else {
        return <div>3</div>
      }
    }
    <div>{getItem()}</div>
    {flag ? <span>渲染</span> : ''}
    <div className={styles.child + ' ' + (item.show ? styles.child_select : '')}></div>
    <div className={styles.child + ' ' + (item.show ? styles.child_select : '')}></div>
    <div className={["title", index === this.state.active?"active":null].join(' ')}></div>
  ```

# 5.JSX语法的转化过程
  - jsx仅仅是createElement方法的语法糖
  - jsx语法被@babel/preset-react插件编译为createElement方法

# 6.classnames,classnames是一个简单的js库，可以方便的通过条件动态控制class类名的显示
  ```js
    import classnames from 'classnames'
    className={`nav-item ${type == item.type && 'active'}`}
    className={classnames('nav-item', {active: type == item.type})}
  ```