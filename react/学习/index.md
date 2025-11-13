#  一：jsx语法


# 二：组件通信
  ### 1.父传子：props,当子组件中间嵌套内容时，父组件可以通过props.children来获取该内容
    ```js
      // 父组件
      <Son
        name={appName}
        isTrue={false}
        list={['Vue','React']}
        cb={() => console.log(123)}
        child={<span>123</span>}
      >this is span</Son>
      function Son (props) {
        console.log(props) // props.children
        return <div>this is son</div>
      }
    ```
  ### 2.子传父
    ```js
      function Son({onGetSonMsg}){
        const sonMsg = 'this is myslef msg'
        return (
          <div>my name is son<button onClick={() => onGetSonMsg(sonMsg)}>sendMsgToFather</button></div>
        )
      }
      function App () {
        const getMsg = (msg) => {
          console.log(msg)
        }
        <Son onGetSonMsg={getMsg} />
      }
    ```

  ### 3.兄弟组件通信
  ### 4.context跨层级通信
  - 1.使用ceateContext方法创建一个上下文对象
  - 2.在顶层组件App中通过ctx.provider组件提供数据
  - 3.在底层组件B中通过useContext钩子函数获取到消费数据
    ```js
      // 相当于一个公共的存储空间，这样无需通过props层层传递，就可以让组件访问到这些数据
      // 当我们通过context访问数据时，他会读取距离他最近的Provider中的数据，如果咩有Provider，则hi读取context中默认数值
      // 使用方式：
      // 第一步：使用ceateContext方法创建一个上下文对象
      import { createContext } from 'react'
      const msgContext = createContext()
      <context.Provider value={{name:'孙悟空',age:18}}></context.provider>
      // 第二步：在顶层组件App中通过ctx.provider组件提供数据
      function App () {
        const msg = 'this is a msg'
        return (
          <div>
            <msgContext.provider>
              this is APP
              <A></A>
            </msgContext.provider>
          </div>
        )
      }
      // 第三步：在底层组件B中通过useContext钩子函数获取到消费数据
      import context from '/store/context'
      const CompB = () => {
        const ctx = useContext(msgContext)
        return (
          <div></div>
        )
      }
    ```
    ```js
      // appContext.js
      import { createContext } from "react";
      const appContext = createContext({
        title:'hello context'
      })
      export default  appContext

      //CreateContext组件
      import Child from './comp/Child'
      import appContext from '../../utils/appContext'
      import { useState } from 'react'

      function CreateContext () {
        const [title, setTitle] = useState({title:'HI'})
        const changeTitle = () => {
          setTitle({title:'Hello'})
        }
        return (
          <div>
            <appContext.Provider value={title}>
              <button onClick={changeTitle}>changeTItle</button>
              <Child></Child>
            </appContext.Provider>
          </div>
        )
      }
      export default CreateContext
    ```

# 

