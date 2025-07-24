# 1. useState使用
  在react中，状态被认为是只读的，我们应该始终**替换它而不是修改它**，直接修改状态不能引发视图更新
  ### (1)更新数据
  1.基本类型：直接传入数据
  2.引用类型：使用函数式更新加扩展运算符，不然会导致数据无法更新成功！！！
  ```js
  [state, dispatch] = useState(initData)

  const [xxx, setXXX] = useState(initValue)
  // initData  有两种情况，第一种情况是非函数，将作为 state 初始化的值。 第二种情况是函数，函数的返回值作为 useState 初始化的值。
  //  dispatch的参数,也有两种情况:
  //  第一种非函数情况，此时将作为新的值，赋予给 state，作为下一次渲染使用;
  //  第二种是函数的情况，如果 dispatch 的参数为一个函数，这里可以称它为reducer，reducer 参数，是上一次返回最新的 state，返回值作为新的 state。
  const [ number , setNumber ] = React.useState(0)
  /* 一个点击事件 */
  const handleClick=()=>{
    setNumber(1)
    setNumber(2)
    setNumber(3)
  }
  const [ number , setNumber ] = React.useState(0)
  const handleClick=()=>{
    setNumber((state)=> state + 1)  // state - > 0 + 1 = 1
    setNumber(8)  // state - > 8
    setNumber((state)=> state + 1)  // state - > 8 + 1 = 9
  }
  ```

# 常见问题
  ### 1.setState真的是异步吗
  ```js
  const [count, setCount] = useState(0)
  function handleClick () {
    setCount(count => {
      return count + 2
    })
    document.title = count // 此处获取的到的count就是上次的数据，未拿到最新获取的数据，说明了setState本身是异步的
  }
  ```
  https://juejin.cn/post/6844903636749778958
  ### 2.state惰性初始化
  如果你要更新的state的前后值相同时，react将跳过子组件的渲染并且不会触发effect的执行
  ```js
  export default function Index(){
    const [ state  , dispatchState ] = useState({ name:'alien' })
    const  handleClick = ()=>{ // 点击按钮，视图没有更新。
        state.name = 'Alien'
        dispatchState(state) // 直接改变 `state`，在内存中指向的地址相同。
    }
    return <div>
         <span> { state.name }</span>
        <button onClick={ handleClick }  >changeName++</button>
    </div>
  }
  // 在 useState 的 dispatchAction 处理逻辑中，会浅比较两次 state ，发现 state 相同，不会开启更新调度任务； demo 中两次 state 指向了相同的内存空间，所以默认为 state 相等，就不会发生视图更新了。

  // 解决问题： 把上述的 dispatchState 改成 dispatchState({...state}) 根本解决了问题，浅拷贝了对象，重新申请了一个内存空间。
  ```
  ### 3.假设setState执行了多次，比如以下场景
  ```js
  const [count, setCount] = useState(0)
  function handleClick () {
    setCount(count => {
      return count + 2
    })
    setCount(count => {
      return count + 1
    })
  }
  ```
  ### 4.如何监听state的变化
  类组件：setState的第二个参数callback或者生命周期componentDidUpdate可以监测到state的变化或者组件的更新
  函数组件：使用useEffect,将state作为依赖项传入useEffect第二个参数deps，但是注意useEffect初始化会默认执行一次。
  ```js
  const [ number , setNumber ] = React.useState(0)
    /* 监听 number 变化 */
    React.useEffect(()=>{
        console.log('监听number变化，此时的number是:  ' + number )
    },[ number ])
    const handerClick = ()=>{
        /** 高优先级更新 **/
        ReactDOM.flushSync(()=>{
            setNumber(2) 
        })
        /* 批量更新 */
        setNumber(1) 
        /* 滞后更新 ，批量更新规则被打破 */
        setTimeout(()=>{
            setNumber(3) 
        })
       
    }
    console.log(number)
    // 执行结果2，1,3
  ```
  ### 5.更新state中的对象和数组：
  当你试图修改state中的对象或者数组的时候，你应该创建一个新的对象或者数组或者使用原来对象的拷贝值来替换她
  **useState 有一点值得注意，就是当调用改变 state 的函数dispatch，在本次函数执行上下文中，是获取不到最新的 state 值的，把上述demo 如下这么改：**
  ```js
  const [ number , setNumber ] = React.useState(0)
  const handleClick = ()=>{
      ReactDOM.flushSync(()=>{
          setNumber(2) 
          console.log(number) 
      })
      setNumber(1) 
      console.log(number)
      setTimeout(()=>{
          setNumber(3) 
          console.log(number)
      })   
  }
  ```
  原因很简单，函数组件更新就是函数的执行，在函数**一次执行**过程中，函数内部所有变量重新声明，所以改变的 state ，只有在下一次函数组件执行时才会被更新。所以**在如上同一个函数执行上下文中**，number 一直为0，无论怎么打印，都拿不到最新的 state 。可以理解为它是一次执行，不会重新执行函数！！
  [!参考链接]https://juejin.cn/book/6945998773818490884/section/6951186955321376775