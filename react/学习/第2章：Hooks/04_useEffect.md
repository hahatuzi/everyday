# 一：基本使用
  ```js
    // 参数一：副作用函数，该函数必须为同步函数，如果要发送异步请求可以在函数内部再声明一个函数
    // 若参数二为空：则每次更新时都会执行useEffect函数   //相当于componentDidMount + DidUpdate
    // 若参数二为空数组[], 执行时机：只执行一次 // 场景ajax请求   //相当于componentDidMount
    // 若参数二指定了依赖项：执行时机：初始化执行一次，依赖项值变化时再执行一次
    useEffect(参数一，参数二)
    useEffect( () => {
      // 副作用函数的内容
      return 清理函数
    }，参数二)

    useEffect(() => {}) // **没有依赖项**时，会在**初始化**和**组件更新**的时候加载
    useEffect(() => {}, []) // 依赖项为**[]**时，会在**初始化**时加载
    useEffect(() => {}, [count]) // 存在特定依赖项时，会在依赖项更新时执行。
    useEffect(() => {//实现副作用操作逻辑 return () => {//清除副作用逻辑}}, [])


    // 比如：
    async function getWeather() {
      try {
        const { data } = await getTodayWeather();
        setWeather(data[0]);
      } catch (error) {
      }
    }
    useEffect(() => {
      getWeather();
    }, []);

    // 副作用函数的返回值的作用：清理副作用，场景：启动和清理定时器，清理事件监听，重置页面数据，清理或还原状态
    // 副作用函数的返回值清理函数的执行时机：组件卸载或者下一次副作用函数执行前
    // 比如：componentWillUnmount,因为组件通常会被多次渲染，因为useEffect是根据state状态来更新的，所以在执行下一个effect之前，上一个effect要被清除即return的函数要被清除
  ```

  ```js
    function Son(){
      useEffect(() => {
        const timer = setInterval(() => {
          console.log('timer')
        },1000)
        return () => {
          clearInterval(timer)
        }
      },[]) // 定时器
      return (
        <div>this is son</div>
      )
    }
    function App () {
      const [show, setShow] = useState(true)
      return (
        <div>
          {show && <Son></Son>}
          <button onClick={() => setShow(false)}>卸载Son组件</button>
        </div>
      )
    }
    // useEffect的定时器的不同写法
    // 写法一：每次更新的时候都会销毁旧的定时器，然后再产生一个新的定时器
    const foo = params => {
      const [count, setCount] = useState()
      useEffect(() => {
        console.log('开启定时器')
        let timer = setInterval(() => {
          console.log('进入定时器')
          setCount(count + 1)
        }, 1000)
        return () => {
          clearInterval(timer)
        }
      })
      return (
        <div></div>
      )
    }
    // 写法二：仅会在didmount的时候产生一个定时器,但是要注意setCount的时候使用箭头函数来获取最新的count
    const foo = params => {
      const [count, setCount] = useState()
      useEffect(() => {
        console.log('开启定时器')
        let timer = setInterval(() => {
          console.log('进入定时器')
          setCount(count => count + 1)
        }, 1000)
        return () => {
          clearInterval(timer)
        }
      },[])
      return (
        <div></div>
      )
    }
  ```
# 二：作用
函数式组件的主作用：根据数据渲染DOM
副作用：数据请求，开启定时器，事件监听，localStorage存取等

# 三：手写定时器
  ```js
    let prev = []
    function useEffect (callback, depsAry) {
      if (Object.propoty.toString().call(callback) != '[object Function]') throw new Error('in not Function')
      if (typeof depsAry == 'undefined') {
        callback()
      } else {
        if (Object.propoty.toString().call(depsAry) != '[object Array]') throw new Error(' is not Array')
        // 将当前依赖项的值和上一次的依赖值做比较，如果不同，调用callback
        let hasChanged = depsAry.every((item, index) => item == prev[index])
        if (!hasChanged) {
          prev = depsAry
          callback()
        }
      }
    }
  ```

# useEffect为什么会执行两次