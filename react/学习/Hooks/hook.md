
# useTransition
```js
const [filterWord, setFilterWord] = useState('')
const [isPending, startTransition] = useTransition()
const change = (e) => {
  startTransition(() => {
    setFilterWord(e.target.value) // start
  })
}
```
# 自定义hook
