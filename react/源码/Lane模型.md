# react lanes模型
  ## 背景：二进制基础
   - 位操作
   - 位运算符： ~,&,|,^,>>,<<
   - 位掩码
  ## lane用来标记任务的优先级
  ## 并发更新：
   - lane模型增加更多的优先级
   - 
# batchUpdate
  > 所有状态更新（无论是同步还是异步，甚至是 Promise、setTimeout、fetch 等）都会被自动批处理
  ## 1.渲染机制
  - 状态更新收集：
    - 当调用 setState 时，React 不会立即触发渲染，而是将更新放入一个队列。
  - 批处理时机：
    - 在事件循环的微任务（microtask）阶段，React 检查队列中是否有多个更新。如果有，就将它们合并为一次更新。
  - 渲染执行：
    - 合并后的状态一次性应用到组件树，触发单次重新渲染。
  ## 2.批处理条件：
  - 调度时机：
    - 如果多个**setState**调用发生在**同一个宏任务**（如 setTimeout 回调）或**微任务**（如 Promise.then）中，React 会将它们合并。
  - 时间间隔：
    - 如果两个**setTimeout**的回调时间错开，React 会认为它们属于不同的批次，无法合并。
  - 并发特性：
    - react 18 的并发渲染引擎会尽量优化，但独立的异步任务仍可能触发多次渲染。
  ## 2.实例
  ```js
    function Dashboard() {
      const [data, setData] = useState({});
      const [loading, setLoading] = useState(false);

      const fetchData = () => {
        setLoading(true);
        setTimeout(() => {
          setData({ value: 42 });
          setLoading(false);
          // React 18: 1次渲染
        }, 1000);
      };

      const handleClick = () => {
        flushSync(() => {
          setCount(c => c + 1); // 立即渲染
        });
        flushSync(() => {
          setCount(c => c + 1); // 立即渲染
        });
        // 结果：2次渲染
      };

      return <button onClick={fetchData}>{loading ? 'Loading...' : data.value}</button>;
    }

  ```
  ```js
    const [count, setCount] = useState(0)
    const [flag, setFlag] = useState(false)
    const handleClick = () => {
        setCount(c++) // 同步更新
        setFlag(flag => !flag)// 同步更新
      setTimeout(() => {
        setCount(c++)
        setFlag(flag => !flag)
        console.log('update')// react18页面只渲染一次，而react17中会渲染两次
      },100)
    }
  ```
# 高优先级更新如何插队
# suspense的实现