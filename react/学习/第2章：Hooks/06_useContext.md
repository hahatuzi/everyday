# 消费方式：
  ### 方式一：useContext
    ```js
      const count = useContext(CountContext)
      <div>{count}</div>
    ```
  ### 方式二：customer
    ```js
    <CountContext.Consumer>{value => <div>{value}</div>}</CountContext.Consumer>
    ```
  ### 方式三：contextType
