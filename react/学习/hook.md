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
# 自定义hook
