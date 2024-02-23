# 1.HOC

# 2.类组件和函数组件的区别

# 3.react-router-dom的路由跳转方式及区别
  ```js
    useNavigate()
    <Link></Link>
  ```

# 4.React.createClass VS extends React.Component
  ### （1）语法使用区别
  ### （2）propType的不同：React.createClass使用getDefaultProps，React.Component使用defaultProps
  ### （3）createClass：getInitState()
  ### （4）Component:constructor
  ### （5）mixin:createClass:mixins添加属性，compoent不能使用mixin

# 5.组件封装案例
  [!参考链接]https://blog.csdn.net/limuzhixing/article/details/129192016

# 6.React事件与 普通的HTML事件的不同
  - 1.事件名称
   - 原生：全小写
   - react:onClick 
  - 2.事件函数处理
    - 原生：字符串
    - react:onClick={}
  - 3.阻止浏览器本身的默认行为
    - 原生:return false
    - react：preventDefault()
  **VDOM 合成事件 模拟原生DOM的行为 cross platfomr react 所有事件全部存放在数组中方便后续操作**
# 7.受控组件和非受控组件的区别
  诸如input,textarea,select这些表单类组件，它们**自身具备状态**，且**可以自身维护状态更新**。
  而我们讲的受控与非受控则指的是：**组件的状态是否可以通过react程序修改**
  [!参考链接]https://www.jianshu.com/p/7edb6982c5a8
  ```js
  import {useState, useRef} from 'react'

  export default function Input() {
      const fileInputRef = useRef<HTMLInputElement>(null)

      const [value, setValue] = useState('')
      
      const handleChange = (e: any) => {
        setValue(e.target.value)
      }
      const handleSubmit = (e: any) => {
        e.preventDefault()  // react阻止浏览器默认行为
        // 消费状态 value
        console.log(value)
        console.log(fileInputRef.current?.value)
      }
    
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
# 8.React.useState为什么使用的是数组而不是对象
  从解构的方面触发
  ```js
    let arr = ['daf','fd',123]
    const [one,two, three] = arr //　只需要索引对应即可，但是对象的解构需要属性名对应才能获取相应的值
    console.log(one, two, three)
    const {id,name} = {id:100,name:'lisa'}
  ```
# 9.react的refs
# 10.react为什么使用hooks
- 提高开发效率：比如在生命周期中逻辑集合
  - 比如我们经常需要在comonentDidMount和componentWillUnmount中使用addEventListener和removeEventListener,这样就会导致逻辑分散。所以我们可以使用useEffect(() => {},[])来避免
- 简化组件封装逻辑复用代码:比如table组件的封装：高阶组件和hooks的不同。
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

# 11.react的降级处理错误边界
# 12.代码分割
webpack rollup  :import和react.lazy
# 13.Fragments
<Fragment> 通常使用 <>...</> 代替，它们都允许你在不添加额外节点的情况下将子元素组合。