```js
h3Ref = createRef()
  <h1 ref="h1ref"></h1>
  <h2 ref={dom => this.h2ref = dom}></h2>
  <h3 ref={this.h3Ref}></h3>
```
# ref操作list
# ref的变更历史
ref, callback ref --> createRef --> useRef,forwardRef转发ref
[!ref理解]https://www.php.cn/faq/499825.html#
[!ref最新使用]https://zhuanlan.zhihu.com/p/478532753

# 单项数据流的原则：谁的状态数据由谁来更新，不应该有父组件或者子组件来更新,而我们ref的使用则打破了这一原则
```js
  function App () {
    const inputRef = useRef()
    handleClick () {
      inputRef.current && inputRef.current.focus()
    }
    return (
      <div>
        <button onClick={() => this.handleClick}></button>
        <input ref={inputRef} placeholder="请输入姓名">
      </div>
    )
  }
```
## useRef的特点：无法获取自定义组件的ref，需要借助forwardRef,但是借助forwarRef后通常获取到的ref是dom元素，通常只能用来修改视图等样式，无法修改state状态数据，所以又产生了useImperativeHandle,让函数组件想外部暴露一些操作方法
```js
function Child1 (props, ref) {
  const [title, setTitle] = useState('child1函数组件')
  const [styleObj, setStyleObj] = useState({})

  console.log(ref.current) // 在这里ref.current为undefined,因为jsx未开始编译
  useImperativeHandle(ref, () => {
    return {
      updateTitle () {
        setTitle('我是child1函数组件')
      },
      setStyle (styleObj){
        setStyleObj(styleObj)
      }
    }
  })
  // useImperativeHandle和forwardRef通常不能同时使用
  useEffect(() => {
    console.log(ref.current)
    // 借助forwarRef后通常获取到的ref是html元素,元素而非dom实例对象，通常只能用来修改视图等样式,子组件外无法直接调用子组件的方法等
    ref.current.style.background = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`
  }, [])
  return (
    <div ref={ref} style={{background:'#EEE', ...styleObj}}>{title}</div>
  )
}
export default forwardRef(Child1)

function UseRef () {
  const childRef1 = useRef()
  const changeChild1 = () => {
    // 借助forwarRef后通常获取到的ref是html元素，而非dom实例对象，通常只能用来修改视图等样式,子组件外无法直接调用子组件的方法等
    childRef1.current.updateTitle()
    childRef1.current.setStyle({color:'red'})
  }
  return (
    <div>
      <button onClick={changeChild1}>改变child1</button>
      <Child1 ref={childRef1}></Child1>
    </div>
  )
}
export default UseRef
```
```js
useImperativeHandle(ref, () => {
  return {
    handle() {

    }
  }
})
```