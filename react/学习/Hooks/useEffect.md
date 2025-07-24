# 4.useEffect实现生命周期
 - 1.useEffect(() => {}),**没有依赖项**时，会在**初始化**和**组件更新**的时候加载
 - 2.useEffect(() => {}, []),依赖项为**[]**时，会在**初始化**时加载
 - 3.useEffect(() => {}, [count]),存在特定依赖项时，会在依赖项更新时执行。
 - 4.useEffect(() => {//实现副作用操作逻辑 return () => {//清除副作用逻辑}}, [])
    ```js
    function Son(){
      useEffect(() => {
        const timer = setInterval(() => {
          console.log('timer')
        },1000)
        return () => {
          clearInterval(timer)
        }
      },[])
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
  ```js
  // 手写useEffect
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