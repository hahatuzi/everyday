# 一：基本概念
  ### 1.惰性初始化:如果你要更新的state的前后值相同时，react将跳过子组件的渲染并且不会触发effect的执行
  ### 2.更新状态变量：
  - (1)不依赖旧数据：state => setState( newState )
  - (2)依赖旧数据：使用state => setState( prev => return newState )，不然会导致数据无法更新成功！！！
  ```js
    const [index, setIndex] = useState<number>(0)
    setIndex(index => index + 1)
  ```
# 二：写法
  ### 写法1：const [状态，函数] = useState(初始值)
  ### 写法2：写法二：const [状态，函数] = useState(回调函数),useState内传入的回调函数的入参：初始值，返回值：初始值经过加工后的新值
  ### 写法3：多个状态：const [状态，函数] =  useState({状态1，状态2})
