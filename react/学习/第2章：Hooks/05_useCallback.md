# 一：基本语法，useCallback():缓存函数，组件多次重新渲染的时候缓存函数
  ```js
    /**
     * 验证是否为blob格式
     * @param {*} fn  想要缓存的函数，React会在初次渲染而非调用时返回改函数，当进行下一次渲染时，如果dependencied相对于上一次的渲染时没有改变，那么React将返回相同的函数
     * @param {*} dependencies  有关是否更新 fn 的所有响应式值的一个列表。
    */
    useCallback(fn, dependencies)
  ```

# 二：使用场景：
  - 在**函数式组件**中，定义在组件内函数会随着状态值的更新而重新渲染，函数中定义的函数会被频繁定义，在父组件的通信中这样是非常消耗性能的，使用useCallback结合memo可以有效的**减少子组件更新的频率**，提高效率。即：当父组件中的状态发生变化时，子组件也会随之更新，即使子组件么有用到发生改变的状态，所以可以使用React.memo()和useCallback()
  ```js
    // useCallback创建的回调函数不会总在组件重新渲染的时候重新创建
    const clickHandler = useCallback(() => {
      setCount(pre => pre + 1)
    })
    const Input = memo(function ({change}) {
      console.log('input子组件重新渲染了')
      return <div><input onChange={( e) => {change(e.target.value)}} /></div>
    })

    function fn () {
      console.log(Math.random())
    }
    const catchFn = React.useCallback(fn, [])
  ```
