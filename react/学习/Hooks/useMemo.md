# useMemo 用来缓存函数的执行结果,当函数不需要组件每次更新的时候都执行的情况下适用。

```js
const cachedValue = useMemo(calculateValue, dependencies);
/*
 * calculateValue,可以把它想象成vue中computed的计算函数，react会在第一次渲染和dependencies变化的时候执行它
 * dependencies，react使用Object.is来判断它是否发生变化
 */
```

**类似于 vue 的 computed**,根据某个值的变化来计算新值

```js
function App() {
  const [count, setCount] = useState(0);
  const result = useMemo(() => {
    return count * 2;
  }, [count]);

  const list = useMemo(() => {
    list.filter((item) => item.type == 1);
  }, [list]);
}
```

```js
function sum(a, b) {
  const begin = Date.now();
  while (true) {
    if (Date.now - begin > 3000) {
      break;
    }
  }
  return a + b;
}
const compA = () => {
  const [count, setCount] = useState(1);
  // const result = sum(11,22)
  const result = useMemo(() => {
    return sum(11, 22);
  }, []);
  return (
    <div>
      <span>{result}</span>---<span>{count}</span>
      <hr></hr>
      <button onClick={() => setCount((prev) => prev + 1)}>add</button>
    </div>
  );
};
const result = useMemo(() => {
  return sum(11, 22);
}, []);
```

# 二：memo 方法

使用 memo 方法进行性能优化，如果本组件中的数据没有发生变化，组织组件更新，类似于类组件中的 PureComponent 和 shouldComponentUpdate

```js
import React, { memo } from "react";
function Counter() {
  return <div></div>;
}
export default memo(Counter);
```
