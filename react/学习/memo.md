React.Memo
react组件重新渲染的场景包括自身的state发生变化或者父组件发生变化两种情况。
React.meno是一个高阶组件，它接收另一个组件作为参数，并且会返回一个包装过的新组件，包装过的新组件就会具有缓存功能。包装过的组件只有组件自身的props发生变化时才会
触发组件而重新渲染，否则总是返回缓存中的数据
```js
const B = () => {
  return (
    <div>B组件</div>
  )
}
export default React.memo(B)
const A = () => {
  return (
    // 
    <div><B show={count === 4}></B></div>
  )
}
```