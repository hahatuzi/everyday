# 一：useRef
  ### 源码
    ```js
      function mountRef<T>(initialValue: T): {|current: T|} {
        const hook = mountWorkInProgressHook();
      
        const ref = {current: initialValue};
        hook.memoizedState = ref;
        return ref;
      } 
      function updateRef<T>(initialValue: T): {|current: T|} {
        const hook = updateWorkInProgressHook();
        return hook.memoizedState;
      }
    ```
  ### 应用场景
  ```js
    const useInterval = (fn:() => void, delay?:number, options:{immediate?: boolean} = {}) => {
      const timerCallback = useMemoizedFn(fn)
      const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

      const clear = useCallback(() => {
        if(timerRef.current){
          clearInterval(timerRef.current)
        }
      }, [])
      useEffect(() => {
        if(!isNumber(delay) || delay < 0){
          return
        }
        if(!options.immediate){
          timerCallback()
          timerRef.current = setInterval(timerCallback, delay)
          return clear
        }
      }, [delay, options.immediate])

      return clear
    }
    export default useInterval
  ```

# 二：useState和useRef的区别
|       特性      |                  useState                |                 useRef                  |
| :-------------: | :---------------------------------------:| :--------------------------------------:|
|       结构      |              [状态，函数]                |                {current:值}             |
|   是否触发渲染  |                   是                     |                     否                  |
|   是否同步更新  |   异步需要useEffect或者下次渲染时更新    |             同步，可立即读取            |
|       用途      |            表单，显隐状态，计数          |  DOM引用，定时器，非渲染依赖，缓存旧值  |