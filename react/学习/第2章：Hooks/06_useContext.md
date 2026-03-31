# 消费方式：
  ### 方式一：useContext
    ```js
      const count = useContext(CountContext)
      <div>{count}</div>
    ```
  ### 方式二：Consumer
    ```js
    <CountContext.Consumer>{value => <div>{value}</div>}</CountContext.Consumer>
    ```
  ### 方式三：contextType:只能在类组件中使用，且只能订阅单一的context来源
    ```js

    ```
