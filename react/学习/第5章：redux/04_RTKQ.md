# 一：介绍
  RTK不仅帮助我们解决了state的问题，同时，它还为我们提供了RTK Query用来帮助我们**处理数据加载**的问题。
  RTK Query是一个强大的数据获取和缓存工具。
  在它的帮助下，Web应用中的加载变得十分简单，它使我们不再需要自己编写获取数据和缓存数据的逻辑。
  Web应用中加载数据时需要处理的问题：

  ### 优点：
  1. 根据不同的加载状态显示不同UI组件
  2. 减少对相同数据重复发送请求
  3. 使用乐观更新，提升用户体验
  4. 在用户与UI交互时，管理缓存的生命周期
  这些问题，RTKQ都可以帮助我们处理。首先，可以直接通过RTKQ向服务器发送请求加载数据，并且RTKQ会自动对数据进行缓存，避免重复发送不必要的请求。
  其次，RTKQ在发送请求时会根据请求不同的状态返回不同的值，我们可以通过这些值来监视请求发送的过程并随时中止。
# 二：使用
  ### 第一步：
  ```js
  const studentApi = createApi({
    reducerPath:'studentApi', // api的标识
    baseQuery: fetchBaaseQuery({
      baseUrl:'http://localhost:80/api/'
    }),
    endpoints(build){
      return {
        getStudentList:build.query({
          query () {
            return 'xxx'
          }
        })
      }
    }
  })
  export const {
    useGetStudentList
  } = studentApi
  export default studentApi
  // =========================详解
  import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react'

  // 创建Api对象
  // createApi() 用来创建RTKQ中的API对象
  // RTKQ的所有功能都需要通过该对象来完成
  const studentApi = createApi({
      reducerPath:'studentApi',    //Api对象的唯一标识
      baseQuery:fetchBaseQuery({  //用来指定查询的工具(方法)
          baseUrl:'http://localhost:1337/api/'
      }),  
      endpoints(build){    // endpoints用来指定Api中的各种功能，是一个方法，需要一个对象作为返回值
          return {
              getStudents:build.query({
                  query(){
                      // 用来指定请求子路径
                      return 'students'   //当调用getStudents方法时，该返回值会和baseUrl拼一起
                  },
                  // transformResponse()用于设置返回的请求对象的内容,该方法可不写
                  transformResponse(baseQueryReturnValue){
                    return baseQueryReturnValue.data
                  }
              })
          }
      }   
  })

  export const {useGetStudentsQuery} = studentApi
  export default studentApi
  ```

  ```js
  import {configureStore} from '@reduxjs/toolkit'
  import studentApi from './studentApi'
  const store = configureStore({
    reducer:{
      [studentApi.reducerPath]:studentApi.reducer
    },
    middleware:getDefaultMiddleware => {
      getDefaultMiddleware().concat(studentApi.middleware)
    }
  })
  setupListeners(store.dispatch)
  export default store
  ```

# 参数解读
1.isFetching:true  数据是否在加载
2.isloading:true  数据是否第一次加载
3.isSuccess:   数据是否加载成功
4.inUninitialized:false   请求是否还没有开始发送
refetch:f()  用来重新加载数据
status:请求的状态