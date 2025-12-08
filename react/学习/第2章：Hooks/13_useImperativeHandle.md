# 父组件通过ref获取子元素的DOM和方法
### 1.获取元素,通过useRef,// 此种方式有可能导致父组件修改了ref的值后，子组件的值仍然是旧的！！！所以出现了useImperativeHandle()
```js
// 子元素
const FocusInput = forwardRef(function (props, ref) {
  return (
    <div><input type='text' ref={ref}></input></div>
  )
})
// 父元素
const App = function () {
  const sonRef = useRef(null)
  const showRef = () => {
    console.log(sonRef)
    sonRef.current.focus()
  }
  return (
    <div>
      <FocusInput ref={sonRef}></FocusInput><button onClick={showRef}>focus</button>
    </div>
  )
}
export default App
```
### 2.获取子元素的方法,通过useRef和useImperativeHandle的结合
```js
const FocusInput1 = forwardRef(function (props, ref) {
  const sonRef1 = useRef(null)
  const focusHandler = () => {
    console.log(sonRef1)
    sonRef1.current.focus()
  }
  useImperativeHandle(ref, () =>{
    return {
      focusHandler
    }
  })
  return (
    <div><input type='text' ref={sonRef1}></input></div>
  )
})
// 父元素
const App = function () {
  const sonRef1 = useRef(null)
  const showRef = () => {
    console.log(sonRef1)
    sonRef1.current.focusHandler()
  }
  return (
    <div>
      <FocusInput1 ref={sonRef1}></FocusInput1><button onClick={showRef}>focus</button>
    </div>
  )
}
export default App
```

# useRef还可以作为稳定的定时器
```js
function App () {
  const timerRef = useRef<number | undefined>(undefined)
  useEffect(() => {
    timerRef.current = setInterval(() => {
      console.log('1')
    })
    return () => {clearInterval(timerRef.current)}
  }, 1000)
  return (
    <div>App</div>
  )
}
```