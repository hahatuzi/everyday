# useReducer学习
```js
useReducer(reducer,initialArg, init)
/*
* reducer:函数
* initialArg:state的初始值，作用和useState中的值一样
* return array
*/
```
```js
// const [state, dispatch] = useReducer(reducer, initialArg,init)
// 第一个参数：state用来获取state的值
// 第二个参数，修改state的派发器，具体的修改行为将会有另外一个函数reducer执行
function reducer(state, action){
  if(action.type === 'incremented_age') {
    return {age:state.age - 1}
  }
  return {age:state.age} //为了避免action出错的情况，我们需要返回一个默认值
}
const [state, dispatch] = useReducer(reducer, {age: 42})

function handleClick(){
  dispatch({type:'incremented_age'})
}
```
**注意**
1.dispatch函数式为**下一次渲染**而更新state，所以在dispatch函数后读取state**并不会拿到更新后的值**
2.为了避免reducer会重复创建，通常reducer会定义在组件的外部

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