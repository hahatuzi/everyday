# 一：CustomRef
  ```js
    // 使用场景,防抖输入
    export function useDebounceRef (value, duration = 1000) {
        let timeout
      return customRef((tract, trigger) => {
        return {
            set (val) {
                clearTimeout(timeout)
                timeout = setTimeout(() => {
                  value = val
                  trigger() // 派发更新
                },duration)
            }
            get () {
                tract()
                return value
            }
        }
      })
    }

    // vue文件
    import useDebounceRef from './useDebounceRef.js'
    const text = useDebounceRef('hello', 3000)
    <input v-model="text">
  ```