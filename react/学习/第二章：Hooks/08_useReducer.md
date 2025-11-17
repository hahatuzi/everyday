# 语法
  ```js
    // 1.reducer:处理状态更新的reducer
    // 2.initialArg:状态初始值
    // 3.init状态初始化函数
    const [state, dispatch] =  useReducer(reducer, initialArg, init)

    import  React, { useReducer }  from  'react'
    function  reducer  (state, action ) {
        switch  (action.type) {
            case 'increment' :
                return  state + 1
        }
    }
    function  App () {
        const  {count, dispatch} = useReducer(reducer, 0)
        return (
            <div>
                <button  onclick={() => dispatch({type:'increment'})}>+1</button>
            </div>
        )
    }
  ```

