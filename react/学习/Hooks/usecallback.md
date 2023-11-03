# useCallback：缓存函数，使得组件重新渲染时得到相同的函数实例
// useCallback创建的回调函数不会总在组件重新渲染的时候重新创建
```js
const clickHandler = useCallback(() => {
  setCount(pre => pre + 1)
})
```
useCallback(fn, dependencies)
// fn 想要缓存的函数，React会在初次渲染而非调用时返回改函数，当进行下一次渲染时，如果dependencied相对于上一次的渲染时没有改变，那么React将返回相同的函数
// dependencies：有关是否更新 fn 的所有响应式值的一个列表。