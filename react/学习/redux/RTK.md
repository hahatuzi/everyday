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
# 第二步，注册store：
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
# 第三步,在组件中使用：
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