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

# 二：**注意**
  - 1.dispatch函数式为**下一次渲染**而更新state，所以在dispatch函数后读取state**并不会拿到更新后的值**
  - 2.为了避免reducer会重复创建，通常reducer会定义在组件的外部

    ```js
        // useReducer和context一起使用
        const [number, dispatchNumber] = useReducer((state,action) => {
        const {payload, name} = action
        switch (name) {
            case 'a':
            return state + 1
            case 'b':
            return state - 1
        }
        })
        <Context.Provider dispatch={dispatchNumber} state={{number}}>
        <Chidlern></Chidlern>
        </Context.Provider>
    ```