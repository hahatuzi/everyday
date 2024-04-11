# 1.HOC

# 2.类组件和函数组件的区别

# 3.react-router-dom 的路由跳转方式及区别

```js
  useNavigate()
  <Link></Link>
```

# 4.React.createClass VS extends React.Component

### （1）语法使用区别

### （2）propType 的不同：React.createClass 使用 getDefaultProps，React.Component 使用 defaultProps

### （3）createClass：getInitState()

### （4）Component:constructor

### （5）mixin:createClass:mixins 添加属性，compoent 不能使用 mixin

# 5.组件封装案例

[!参考链接]https://blog.csdn.net/limuzhixing/article/details/129192016

# 6.React 事件与 普通的 HTML 事件的不同

- 1.事件名称
- 原生：全小写
- react:onClick
- 2.事件函数处理
  - 原生：字符串
  - react:onClick={}
- 3.阻止浏览器本身的默认行为
  - 原生:return false
  - react：preventDefault()
    **VDOM 合成事件 模拟原生 DOM 的行为 cross platfomr react 所有事件全部存放在数组中方便后续操作**

# 7.受控组件和非受控组件的区别

诸如 input,textarea,select 这些表单类组件，它们**自身具备状态**，且**可以自身维护状态更新**。
而我们讲的受控与非受控则指的是：**组件的状态是否可以通过 react 程序修改**
[!参考链接]https://www.jianshu.com/p/7edb6982c5a8

```js
import { useState, useRef } from "react";

export default function Input() {
  const fileInputRef = useRef < HTMLInputElement > null;

  const [value, setValue] = useState("");

  const handleChange = (e: any) => {
    setValue(e.target.value);
  };
  const handleSubmit = (e: any) => {
    e.preventDefault(); // react阻止浏览器默认行为
    // 消费状态 value
    console.log(value);
    console.log(fileInputRef.current?.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        名字:
        <input type="text" value={value} onChange={handleChange} />
        {/* 在这里我们使用了handleChange方法来修改名字input的状态，那么这个input组件在这里就被被当做受控组件来使用了 */}
      </label>
      <label>
        请选择文件:
        <input type="file" ref={fileInputRef} />
        {/* 这里我们仅通过ref获取了input的状态，并咩有使用react的任何方法去修改状态，所以这样的使用场景就称为非受控组件 */}
      </label>
      <input type="submit" value="提交" />
    </form>
  );
}
```

# 8.React.useState 为什么使用的是数组而不是对象

从解构的方面触发

```js
let arr = ["daf", "fd", 123];
const [one, two, three] = arr; //　只需要索引对应即可，但是对象的解构需要属性名对应才能获取相应的值
console.log(one, two, three);
const { id, name } = { id: 100, name: "lisa" };
```

# 9.react 的 refs

# 10.react 为什么使用 hooks

- 提高开发效率：比如在生命周期中逻辑集合
  - 比如我们经常需要在 comonentDidMount 和 componentWillUnmount 中使用 addEventListener 和 removeEventListener,这样就会导致逻辑分散。所以我们可以使用 useEffect(() => {},[])来避免
- 简化组件封装逻辑复用代码:比如 table 组件的封装：高阶组件和 hooks 的不同。

  ```js
    componentDidMount(){this.loadData()}
    loadData = () => {this.setState({current:1,total:20, pageSize:10,dataSource:[]})}
    onTableChange = () => {this.setState({current:1,total:20, pageSize:10,dataSource:[]})}
    render(){
      const {total, pageSize, current, dataSource} = this.state
      return <Table dataSource={dataSource} pagination={total, pageSize, current} onChange={this.onTableChange}></Table>
    }
    // 高阶组件的封装方法:祖父 -> 父 -> 子 层层嵌套
    function useTable(){
      return function (WrappedComponent) {
        return class HighComponent extends React.Component {
          state = {tableProps: XXX}
          render () {
            const {tableProps} = this.state
            return <WrappedComponent tableProps={tableProps}></WrappedComponent>
          }
        }
      }
    }
    @useTable
    class App extends Component{
      const {tableProps} = this.props
      render(){
        return <Table columns={} {...tableProps}></Table>
      }
    }

    // hooks实现
    function useTable(){
      const [tableProps, setTableProps] = useState(XXX)
      return tableProps
    }
    function App () {
      const {tableProps} = useTable()
      return <Table columns={} {...tableProps}></Table>
    }
  ```

# 11.react 的降级处理错误边界

# 12.代码分割

webpack rollup :import 和 react.lazy

# 13.Fragments

<Fragment> 通常使用 <>...</> 代替，它们都允许你在不添加额外节点的情况下将子元素组合。

# 14.useEffect 和 useLayoutEffect 的区别

useEffect:组件更新挂载完成后 VDOM --> DOM 更新 --> useEffect :造成页面闪动
useLayoutEffect:组件更新挂载完成后 VDOM --> useLayoutEffect --> DOM 更新 : 造成页面卡顿
useLayoutEffect **内部的代码和所有计划的状态更新阻塞了浏览器重新绘制屏幕**。如果过度使用，这会使你的应用程序变慢。如果可能的话，尽量选择 useEffect。

# 15.useMemo 和 useCallback 的区别

useMemo 返回 callback 的运行结果
useCallback 返回的 callback 的函数

```js
const Demo = () => {
  cosnt[(number, setNumber)] = useState(0);
  const getResult = useMemo(() => {
    const log = () => {
      console.log(number);
    };
  }, [number]);
  return (
    <div>
      <div
        onClick={() => {
          getResult();
        }}
      >
        获取最新值
      </div>
      {/* 使用useMemo获取到了最新值 */}
      <span onClick={() => setNumber(number + 1)}>+1</span>
    </div>
  );
};
```

# 16.fiber

# 17.state 和 props 数据的区别

state 状态是类组件内部定义的数据，可读可写
props 数据是父组件传递给子组件的数据，对子组件来说是只读数据，不能在子组件内修改

```js
class ParentComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      childData: 0,
    };
  }
  // 更新子元素的状态
  updateChildData = (data) => {
    this.setState({
      childData: data,
    });
  };
  render() {
    return (
      <div>
        <ChildComponent
          childData={this.state.childData}
          updateChildData={this.updateChildData}
        />
      </div>
    );
  }
}
class ChildComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: this.props.childData,
    };
  }
  // 点击按钮时调用父元素传递过来的回调函数
  handleClick = () => {
    this.props.updateChildData(this.state.count + 1);
  };
  render() {
    return (
      <div>
        <h2>Child Component</h2>
        <p>Child data: {this.state.count}</p>
        <button onClick={this.handleClick}>Update child data</button>
      </div>
    );
  }
}
```

# 18.React 中的 this 指向问题

```js
update3=() => {
  // 使用箭头函数改变this指向
}
<div onClick={() => this.update1()}></div>
<div onClick={this.update2.bind(this)}></div>
<div onClick={this.update3}></div>
```

# 19.useEffect 中为什么不能使用 async
