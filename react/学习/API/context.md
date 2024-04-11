# 1.使用

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
