# 变量绑定
# 列表绑定
# 事件绑定
  ```js
    export function App: JSX.Element(){
      return (
        <div>
          <button onClick={(e: MouseEvent<HTMLButtonElement>) => console.log(e.target)}>click</button>
        </div>
      )
    }
  ```