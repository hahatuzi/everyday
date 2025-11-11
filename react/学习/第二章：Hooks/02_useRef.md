# 一：使用步骤
  ### 第一步：调用useRef(初始值)函数，得到引用对象
  ### 第二步：将引用对象通过ref属性添加给任意元素
  ### 第三步：通过引用对象.current获取值
    ```js
      import {useRef, RefObject} from 'react'
      const ref:refObject<number> = useRef<number>(0)
      function fn ():void {
        console.log(ref.current)
        ref.current += 1
      }
      // echarts使用步骤
      const  chartRef = useRef(null)
      const chartDom = chartRef.current
      const myChart = echarts.init(chartDom)


      <button obClick={fn}>click</button>
      <span>{ ref.current }</span>
    ```


# 二：使用场景
  ### 场景一：倒计时
    ```js
      const timer = useRef()
      const [cout, setCount] = useState()
      useEffect(() => {
          timer.current = setInterval(()=>{
              setCount((count)=>{count-1})
          },1000)
        return clearInterval(timer)
      })
    ```
  ### 场景二：在多次渲染之间共享数据
    ```js
      const nameRef =  useRef()
      function fn () {
        nameRef.current = 'lisa'
      }
    ```
  ### 场景三：监听div滚动事件
   ```js
    const peopleRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
      if(['居住人口（个）'].includes(screenModule.name)) {
        getPeopleList()
        if (peopleRef.current){
          peopleRef.current.addEventListener('scroll', (val) => {
            handleScroll(val)
          })
        }
      }
      return () => {
        peopleRef.current?.removeEventListener('scroll', handleScroll)
      }
    },[screenModule.name])
   ```