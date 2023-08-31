```js
function APP () {
  console.log('render')// 会在组件初次加载或者更新的时候调用
  useEffect(() => {
    console.log('effect') // didmount,didUpdate
  },)
  return ()
}
```
# 事件传参
```js

```
# 组件通信
组件间通信方式总结
## 一：父组件 => 子组件：
(1)Props
```js
const Child = ({ name }) => {
    <div>{name}</div>
}

class Parent extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            name: 'zach'
        }
    }
    render() {
        return (
            <Child name={this.state.name} />
        )
    }
}
```
(2)Instance Methods
## 二：子组件 => 父组件：
(1)Callback Functions
(2)Event Bubbling
## 三：兄弟组件之间：
(1)Parent Component
## 四：不太相关的组件之间：
### (1)Context
  ```js
  // 相当于一个公共的存储空间，这样无需通过props层层传递，就可以让组件访问到这些数据
  // 当我们通过context访问数据时，他会读取距离他最近的Provider中的数据，如果咩有Provider，则hi读取context中默认数值
  // 使用方式：
  // 第一步：在App.js中通过React.createContext()创建context
  // const context = React.createContext({
  //   name:'孙悟空',
  //   age:18
  // })
  // export default context
  const context = React.createContext()
  <context.Provider value={{name:'孙悟空',age:18}}></context.provider>
  // 第二步：使用context
  // 使用context的方式一
  import context from '/store/context'
  const CompA = () => {
    return (
      <context.Consumer>{(ctx) => {ctx.name---ctx.age}}</context.Consumer>
    )
  }
  // 使用context的方式二
  import context from '/store/context'
  const CompB = () => {
    const ctx = useContext(context)
    return (
      <div></div>
    )
  }
  ```
Portals
Global Variables
Observer Pattern
Redux等