# useMemo用来缓存函数的执行结果,当函数不需要组件每次更新的时候都执行的情况下适用。
```js
function sum(a,b){
  const begin = Date.now()
  while(true){
    if (Date.now - begin > 3000) {
      break
    }
  }
  return a + b
}
const compA = () => {
   const [count, setCount] = useState(1)
  // const result = sum(11,22)
  const result = useMemo(() => {
    return sum(11,22)
  },[])
   return (
    <div>
      <span>{result}</span>---<span>{count}</span>
      <hr></hr>
      <button onClick={() => setCount(prev => prev+1)}>add</button>
    </div>
  );
}
const result = useMemo(() => {
  return sum(11, 22)
},[])
```