# 一：useMemo的使用

  - 1.useMemo传入的函数内部需要有返回值
  - 2.useMemo只能声明在函数式组件内部,但是react.memo()是直接包裹在函数式组件的外部，类似于computed
  - 3.如果不使用useMemo缓存，那么每次APP组件重新渲染的时候list的引用都会指向一个新的引用，从而导致子组件重新渲染
    ```js
      /*
      * calculateValue,可以把它想象成vue中computed的计算函数，react会在第一次渲染和dependencies变化的时候执行它
      * dependencies，react使用Object.is来判断它是否发生变化
      */
      const cachedValue = useMemo(calculateValue, dependencies);
      // 使用场景
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
    ```

# 二：memo 方法
  - 使用 memo 方法进行性能优化，如果本组件中的数据没有发生变化，组织组件更新，类似于类组件中的 PureComponent 和 shouldComponentUpdate
  -  react的默认渲染机制：**只要父组件重新渲染**，**子组件**就会**无脑渲染**。react组件重新渲染的场景包括：自身的state发生变化或者父组件发生变化两种情况。
  - React.meno是一个高阶组件，它接收另一个组件作为参数，并且会返回一个包装过的新组件，包装过的新组件就会具有缓存功能。
  - 包装过的组件**只有组件自身的props发生变化时**才会触发组件而**重新渲染**，否则总是返回缓存中的数据
    ```js
      import React, { memo } from "react";
      function Counter() {
        return <div></div>;
      }
      export default memo(Counter);
    ```

# 三：useMemo和useCallback的区别
  prop为简单类型,
  Object.is(3,3) ==> 没有变化
  prop为引用类型,比较的是新值和旧值的引用是否相等！！当父组件的函数重新执行时，父组件内的引用类型数组实际上是创建了一个新的引用,如果想保证引用稳定，可以使用useMemo缓存
  Object([],[]) => false 有变化，React值关心引用是否变化
  ```js
    import {memo, useState} from 'react'

    const Son = function () {
      console.log('子组件渲染了') // 不适用memo包裹的组件会无脑跟随父组件渲染
      return (
        <div>son</div>
      )
    }
    const Memoson = memo(function ({count}) {
      console.log('memo子组件渲染了')
      return (
        <div>Memoson {count}</div>
      )
    })
    const Memoson2 = memo(function ({list}) {
      console.log('memo子组件2渲染了')
      return (
        <div>Memoson2 {list}</div>
      )
    })
    const Input = memo(function ({change}) {
      console.log('input子组件重新渲染了')
      return <div><input onChange={( e) => {change(e.target.value)}} /></div>
    })

    const App = function () {
      const [count, setCount] = useState(1)
      const list = useMemo(() => {return [1,2,3]})  // 如果不使用useMemo缓存，那么每次APP组件重新渲染的时候list的引用都会指向一个新的引用，从而导致子组件重新渲染
      const changeHandler = useCallback((value) => console.log(value)) // useCallback也是同样的道理，与useMemo不同的是useCallback用来缓存函数，useMemo用来缓存其他引用类型
      return (
        <div>
          <button onClick={() => setCount(count+1)}>++</button>
          <Son></Son>
          <Memoson count={count}></Memoson>
          <Memoson2 list={list}></Memoson2>
          <Input change={changeHandler}></Input>
        </div>
      )
    }
    export default App
  ```