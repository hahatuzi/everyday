# 1.hook规则
不要在循环，条件或者嵌套函数中调用hook,因为需要确保Hook在每一次渲染中都能按照同样的顺序被调用。
为什么需要保证相同的顺序呢？因为当存在多个hook时，比如多个useState时，组件是如何保证修改的是同一个状态呢？答案是hook的书写顺序。
```js
import React, {useState,useEffect, useRef} from 'react'
const Study = () => {
  const [name, setName] = useState('lisa')
  if (name !== '') {
    useEffect(()=> {
      console.log(name)
    })
  }
  setName('')
  const [curname, setCurname] = useState('rose')
  useEffect(() => {
    console.log(name + '  ' + curname)
  })
  console.log('更新')
  return (
    <div>
      <div onCli></div>
    </div>
  )
}
export default Study
```
# 2. useState使用
(1)更新数据
1.基本类型：直接传入数据
2.引用类型：使用函数式更新加扩展运算符，不然会导致数据无法更新成功！！！
# 3.state惰性初始化
如果你要更新的state的前后值相同时，react将跳过子组件的渲染并且不会触发effect的执行
# 4.useEffect实现生命周期
```js
//componentDidMount() 组件首次加载
//componentWllUnmount() 组件被卸载
useEffect(() => {
  retutn () => {} // 因为组件通常会被多次渲染，因为useEffect是根据state状态来发生更新的，所以在执行下一个effect之前，上一个effect要被清除即return的函数要被清除
}, []) // 当第二个参数为空数组时，表示该副作用不依赖任何值的变化，仅会在页面首次加载的时候执行
// componentDidUpdate() 组件更新后呗立即调用，可以实现props改变时的监听
useEffect( () => {
  //userId变化后的处理逻辑
},[userId])
```