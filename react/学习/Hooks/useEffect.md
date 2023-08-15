# 4.useEffect实现生命周期
```js
//componentDidMount() 组件首次加载
//componentWllUnmount() 组件被卸载
//componentDidUpdate() 组件更新后呗立即调用，可以实现props改变时的监听
useEffect(() => {
  retutn () => {} // 因为组件通常会被多次渲染，因为useEffect是根据state状态来发生更新的，所以在执行下一个effect之前，上一个effect要被清除即return的函数要被清除
}, []) // 当第二个参数为空数组时，表示该副作用不依赖任何值的变化，仅会在页面首次加载的时候执行
useEffect( () => {
  //userId变化后的处理逻辑
},[userId])
```
```js
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