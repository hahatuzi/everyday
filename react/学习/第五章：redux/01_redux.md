# redux三大原则
  - 1.单一数据源：整个应用的state被存储在一棵object tree中
  - 2.state是只读的，唯一改变state的方法就是触发action
  - 3.使用纯函数来执行修改，为了描述action是如何改变state tree 的需要编写reducer

# redux三大概念：
  ### 1.state
   - 1.DomainDate:可以理解为服务器端的数据，比如token
   - 2.UI State:决定当前UI展示的状态
   - 3.App State: APP级别的状态，比如路由状态信息
  ### 2.action
  ### 3.reducer
    ```js
      const initialState = {
        value: 0
      }
      function counterReducer(state = initialState, action) {
        switch(action.type) {
          case 'incream':
            return { ...state, value: state.value + 1}
          case 'decream':
            return { ...state, value: state.value - 1}
        }
      }
      const store = Redux.createStore(counterReducer)
      consolee.log(store)
    ```
  ### 四：Store:对象，将action和reducer联系在一起
  - 维护应用的状态，获取状态**getState()**获取state
  - 状态更新时:需要分发action，**dispatch()**发送action