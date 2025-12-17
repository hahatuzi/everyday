# 一：hooks规则
  - 不要在**循环**，**条**件或者**嵌套函数**中调用hook,因为**需要确保Hook在每一次渲染中**都能**按照同样的顺序**被调用。
  - 为什么需要保证相同的顺序呢？因为当存在多个hook时，比如多个useState时，组件是如何保证修改的是同一个状态呢？答案是hook的书写顺序。
  ```js
    const useCount = params => {
      const [count, setCount] = useState(0)
      useEffect(() => {
        document.title = `Hello World${count}`
      })
      return [count, setCount]
    }
    const foo = params => {
      const [count, setCount] = useCount()
      useEffect(() => {
        console.log('effect')
      })
      return (
        <div></div>
      )
    }
  ```
# 