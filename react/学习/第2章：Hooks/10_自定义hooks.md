# React自定义钩子函数
react中的钩子函数只能在函数组件或者自定义狗子中调用
当我们需要将react中钩子函数提取到一个公共区域时，就可以使用自定义钩子函数，自定义钩子函数其实就是一个普通函数，只是名字以use开头而已
  ```js
    // 定义
    export default function useFetch(){
      const [data, setData] = useState([])
      const [loding, setLoading] = useState(false)
      const [error, setError] = useState(null)

      const fetchData = useCallback(async () => {
        try{
          setLoding(true)
          setError(null)
          const res = await fetch('')
        } catch (error) {
          setError(error)
        }
      })
    }
    // 使用
    const {data,loading,error} = useFetch()
  ```

# 例子
  ```js
    import { useEffect, useState } from "react"

    function useChannel() {
      const [channelList, setChannelList] = useState([])
      useEffect(() =>{
        setChannelList([])
      },[])
      return {
        channelList
      }
    }
    export {useChannel}
    // 使用方法：
    import {useChannel} from 'XXX'
    const App = () => {
      const {channelList} = useChannel()
      return (
        <div>
          {channelList.map(item => <span>{item.label}</span>)}
        </div>
      )
    }
  ```