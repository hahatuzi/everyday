# useOutletContext:当父路由组件使用 outlet 时，可以通过 context 属性向子组件传递数据，子组件可以通过 useOutletContext 接收数据。

```js
  function Parent() {
    return <Outlet context={[count, setCount]}></Outlet>;
  }

  function child() {
    const [count, setCount] = useOutletContext();
    return <div>{count}</div>;
  }
```
