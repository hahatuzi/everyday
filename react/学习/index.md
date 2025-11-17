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

  ### 5.store
  ```js
  npm i react-redux
    // store--index.ts
    import { configureStore } from '@reduxjs/toolkit';
    import {screenReducer} from './screenReducer';
    const store = configureStore({
      reducer:{
        screenModule:screenReducer,
      }
    })
    export default store;
    // store--screenReducer.ts
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
    // PeopleDialog.tsx
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
