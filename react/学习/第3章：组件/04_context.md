# context跨层级通信，context主要用于多个层级的组件想要访问同一个数据的时候
  - 第一步:使用ceateContext方法创建一个上下文对象
  - 第二步:在顶层组件App中通过ctx.provider组件提供数据
  - 第三步:在底层组件B中通过useContext钩子函数获取到消费数据
    ```js
      // 相当于一个公共的存储空间，这样无需通过props层层传递，就可以让组件访问到这些数据
      // 当我们通过context访问数据时，他会读取距离他最近的Provider中的数据，如果咩有Provider，则hi读取context中默认数值
      // 使用方式：
      // 第一步：使用ceateContext方法创建一个上下文对象
      // context-msgContext.js文件
      import { createContext } from 'react'
      const msgContext = createContext()
      export default msgContext
      // 第二步：在顶层组件App中通过ctx.provider组件提供数据
      import msgContext from '@/context/msgContext.js'
      function App () {
        // 共享变量管理在顶层组件
        const [module, setModule] = useState({
          moduleName: 'xx',
          moduleShow:false
        })
        const setModuleInfo = (data) => {
          let {moduleName, moduleShow} = data
          setModule({
            moduleName,
            moduleShow
          })
        }
        return (
          <div>
            <msgContext.provider value={{...module, setModuleInfo}}>
              <CompA onChangeModule={setModuleInfo}></CompA>
              <CompB></CompB>
            </msgContext.provider>
          </div>
        )
      }
      // 第三步：在底层组件B中通过useContext钩子函数获取到消费数据
      import msgContext from '@/context/msgContext.js'
      const CompB = () => {
        const ctx = useContext(msgContext)
        return (
          <div>{ctx.moduleName}</div>
        )
      }
      // 第四步：在A组件中修改ctx中修改数据，其实是触发ctx向下传递的方法setModuleInfo
      import msgContext from '@/context/msgContext.js'
      const CompA = (props) => {
        const ctx = useContext(msgContext)
        const handleClick = () => {
           ctx.setModuleInfo({moduleName: '模块1', moduleShow:true})
        }
        return (
          <button onClick={handleClick}>change Module</button>>
        )
      }
    ```

