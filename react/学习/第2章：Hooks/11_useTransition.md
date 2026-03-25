# useTransition
  > 允许将状态转换标记为非阻塞，并允许其他更新中断它
  ```js
    const [filterWord, setFilterWord] = useState('')
    const [isPending, startTransition] = useTransition()
    const change = (e) => {
      startTransition(() => {
        setFilterWord(e.target.value) // start
      })
    }
  ```