# 一：基本概念
  ### 1.惰性初始化:如果你要更新的state的前后值相同时，react将跳过子组件的渲染并且不会触发effect的执行
  ### 2.更新状态变量：
  - (1)不依赖旧数据：state => setState( newState )
  - (2)依赖旧数据：使用state => setState( prev => return newState )，不然会导致数据无法更新成功！！！
    ```js
      const [index, setIndex] = useState<number>(0)
      setIndex(index => index + 1)
    ```
  ### 3.setState的异步特性
    ```js
      const [count, setCount] = useState(0)
      function handleClick () {
        setCount(count => {
          return count + 2
        })
        document.title = count // 此处获取的到的count就是上次的数据，未拿到最新获取的数据，说明了setState本身是异步的
      }
    ```
    [!参考文章]https://juejin.cn/post/6844903636749778958
# 二：写法
  ### 写法1：const [状态，函数] = useState(初始值)
  ### 写法2：写法二：const [状态，函数] = useState(回调函数),useState内传入的回调函数的入参：初始值，返回值：初始值经过加工后的新值
  ### 写法3：多个状态：const [状态，函数] =  useState({状态1，状态2})
    ```js
      [state, dispatch] = useState(initData)
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