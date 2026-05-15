# 一：案例一：
  ### 第一步：
    ```js
      const { createSlice } = require("@reduxjs/toolkit");
      const userInfoSlice = createSlice({
        name:'userInfo',
        initialState:{
          username:'lisa',
          age:18
        },
        reducers:{
          setName(state, action) {
            state.username = 'rose'
            console.log(state)
          }
        }
      })

      export const {reducer: userInfoReducer } = userInfoSlice
      export const {setName} = userInfoSlice.actions
    ```
  ### 第二步，注册store：
    ```js
      import {userInfoReducer} from './userInfoSlice'
      const {configureStore} = require("@reduxjs/toolkit")

      const store = configureStore({
        reducer:{
          userInfo:userInfoReducer,
        }
      })
      export default store
    ```
  ### 第三步,在组件中使用：
    ```js
      import { useDispatch, useSelector } from 'react-redux'
      import {setName} from './store/userInfoSlice'
      function Test () {
        const userInfo = useSelector(state => state.userInfo)
        const dispatch = useDispatch()
        const changeName = () => {
          dispatch(setName('rose'))
        }
        return (
          <div>
            <div>
              <span>{userInfo.username}---{userInfo.age}</span>
            </div>
            <button onClick={changeName}>修改姓名</button>
          </div>
        )
      }
      export default Test
    ```

# 案例二：
 ```js
    // 第一步：npm i react-redux
    // 第二步：创建：store--index.ts
    import { configureStore } from '@reduxjs/toolkit';
    import {screenReducer} from './screenReducer';
    const store = configureStore({
      reducer:{
        screenModule:screenReducer,
      }
    })
    export default store;
    // 第三步：创建store--screenReducer.ts
    import { createSlice } from "@reduxjs/toolkit";
    const screenSlice = createSlice({
      name:'screenModule',
      initialState:{
        name:'',
        show:false
      },
      reducers:{
        setModule(state, action) {
          let {name, show} = action.payload
          state.name = name
          state.show = show
        }
      }
    })

    export const {reducer: screenReducer } = screenSlice
    export const {setModule} = screenSlice.actions
    // 第四步：在组件中使用PeopleDialog.tsx
    import { useSelector } from 'react-redux';

    type GetStateType = typeof store.getState

    const PeopleDialog = () => {
      const screenModule = useSelector((state: ReturnType<GetStateType>) => state.screenModule)

      useEffect(() => {
        if(['居住人口（个）'].includes(screenModule.name)) {
          getPeopleList()
          setTimeout(() => {
            communityBoundary()
          }, 1000);
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
    }
    // index.tsx
    import { useDispatch, useSelector } from 'react-redux'
    type GetStateType = typeof store.getState
    const Left = () => {
      
      const screenModule = useSelector((state: ReturnType<GetStateType>) => state.screenModule)
      console.log(screenModule.name);
      
      const dispatch = useDispatch()
      const handleFn = (data:ModuleItem) => {
        dispatch(setModule({name: data.name, show:data.show}))
      }
    }
  ```