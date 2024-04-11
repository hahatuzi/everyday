# react的默认渲染机制：只要父组件重新渲染，子组件就会无脑渲染。react组件重新渲染的场景包括：自身的state发生变化或者父组件发生变化两种情况。
# 一：React.memo
React.meno是一个高阶组件，它接收另一个组件作为参数，并且会返回一个包装过的新组件，包装过的新组件就会具有缓存功能。
包装过的组件**只有组件自身的props发生变化时**才会触发组件而**重新渲染**，否则总是返回缓存中的数据
```js
// 写法
const MemoComponent = memo(function SomeComponnet (props) {

})
```
```js
import {memo, useState} from 'react'
const MemoSon = memo(function Son () {
  console.log('我是子组件，我重新渲染了')
  return <div>son</div>
})

function  App () {
  const [count, setCount] = useState()
  return (
    <div className="App">
      <button onClick={() => setCount(count + 1)}> ++ </button>
      <MemoSon show={count === 4}></MemoSon>
    </div>
  )
}
```
# 二：React.memo--props的比较机制：
  **在使用memo缓存组件之后，React会对每一个prop使用Object.is比较新值和老值，返回true表示没有变化**
# 三：useMemo
  如果不使用useMemo缓存，那么每次APP组件重新渲染的时候list的引用都会指向一个新的引用，从而导致子组件重新渲染
# 四：usecallback 
  prop为简单类型,
  Object.is(3,3) ==> 没有变化
  prop为引用类型,比较的是新值和旧值的引用是否相等！！当父组件的函数重新执行时，父组件内的引用类型数组实际上是创建了一个新的引用,如果想保证引用稳定，可以使用useMemo缓存
  Object([],[]) => false 有变化，React值关心引用是否变化
  ```js
    import {memo, useState} from 'react'

    const Son = function () {
      console.log('子组件渲染了') // 不适用memo包裹的组件会无脑跟随父组件渲染
      return (
        <div>son</div>
      )
    }
    const Memoson = memo(function ({count}) {
      console.log('memo子组件渲染了')
      return (
        <div>Memoson {count}</div>
      )
    })
    const Memoson2 = memo(function ({list}) {
      console.log('memo子组件2渲染了')
      return (
        <div>Memoson2 {list}</div>
      )
    })
    const Input = memo(function ({change}) {
      console.log('input子组件重新渲染了')
      return <div><input onChange={( e) => {change(e.target.value)}} /></div>
    })

    const App = function () {
      const [count, setCount] = useState(1)
      const list = useMemo(() => {return [1,2,3]})  // 如果不使用useMemo缓存，那么每次APP组件重新渲染的时候list的引用都会指向一个新的引用，从而导致子组件重新渲染
      const changeHandler = useCallback((value) => console.log(value)) // useCallback也是同样的道理，与useMemo不同的是useCallback用来缓存函数，useMemo用来缓存其他引用类型
      return (
        <div>
          <button onClick={() => setCount(count+1)}>++</button>
          <Son></Son>
          <Memoson count={count}></Memoson>
          <Memoson2 list={list}></Memoson2>
          <Input change={changeHandler}></Input>
        </div>
      )
    }
    export default App
  ```