```js
const inputRef = useRef()
const click = () => {
  console.log(inputRef.current.value)
}
<div>
<input ref="inputRef"></div>
<button onClick={() => click}></button>
</div>
// 当需要再父组件中获取ref的话怎么办呢，ref获取的是原生DOM对象，无法在自定义组件上使用比如<compA ref="compARef"></compA>
```
```js
const compA = React.forwardRef((props, ref) => {
  const inputRef = useRef()
  return (
    <div>
      <h2 ref={ref}></h2>
      <input ref="inputRef"></div>
      <button onClick={() => click}></button>
    </div>
  )
})
// 此种方式有可能导致父组件修改了ref的值后，子组件的值仍然是旧的！！！所以出现了useImperativeHandle()
```
```js
const compA = React.forwardRef((props, ref) => {
  const inputRef = useRef()
  useImperativeHandle(ref, () => {
    return {
      changeValue (val) {
        inpurRef.current.value = val
      }
      // 通常返回一个操作DOM的方法，而不是直接返回DOM
    }
  })
  return (
    <div>
      <h2 ref={ref}></h2>
      <input ref="inputRef"></div>
      <button onClick={() => click}></button>
    </div>
  )
})
// 父组件
compA.current.changeValue(count)
<compA ref="compARef"></compA>
```