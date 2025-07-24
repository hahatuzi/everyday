
# react中的css解决方案
  ### 方案一：内联样式的写法；
    ```js
      const Hello = () => {
        const [color,setColor] = useState(true)
        const HelloStyle = {
          color: color ? 'red' : 'blue'
        }
        const changeColor = () => {
          setColor(false)
        }
        return (
          // 1.完全内联
          // <div  style={{color:'red'}}>Hello</div>
          // 2.通过变量来控制内联
          <div  style={HelloStyle}>Hello</div>
          <button onClick={changeColor}></button>
        )
      }
      export default Hello
    ```
  ### 方案二：普通的css写法；
    ```js
      // 外联样式，此等情况下可能会导致样式污染！！它属于全局样式，并非模块样式
      import './index.css'
      const Hello = () => {
        return (
          <div className="title">title</div>
        )
      }
      export default Hello
    ```
  ### 方案三：css modules；
  ### 方案四：css in js（styled-components）；


[!参考链接]https://zhuanlan.zhihu.com/p/156806997

