react router可以将url地址和组件进行映射
当用户访问某个地址时，与之对应的组件会自动挂载，
当我们通过点击Link构建的链接进行跳转时，跳转并没有经过服务器，所以没有问题，但是当我们刷新页面，或者通过普通链接进行跳转的时候，
会向服务器发送请求，这时的请求并没有经过react router所以会返回404
# 解决方案
1.使用HashRouter,服务器不会去判断hash值
所以使用HashRouter后请求将会有React Router来处理
2.修改服务器的配置，将所有请求都转发到index.html

# 二：router改写
```js
    // ========================新的写法：使用useRoutes()===============================
    // https://blog.csdn.net/qq_30769437/article/details/128149273
    // 第一步：将路由配置表写成懒加载模式
    import {Navigate} from 'react-router-dom'
    import  {lazy, Suspense} from 'react'

    const Test1 = lazy(() => import('@/components/test1/test1'))

    const withLoadingComponent = (comp:JSX.Element) => {
      return <Suspense fallback={<div>loading...</div>}>{comp}</Suspense>
    }

    const routes = [
      {path:"/",element:<Navigate to="/"></Navigate>}, // 重定向路由
      {path:"/test1",element:withLoadingComponent(<Test1></Test1>)},
    ]
    export default routes
    // 第二步：在main.js中声明路由模式是hash还是history
    import React from 'react'
    import ReactDOM from 'react-dom/client'
    import 'reset-css'
    import App from './App.tsx'
    import '@/styles/global.scss'
    import { BrowserRouter} from "react-router-dom"

    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <BrowserRouter>
          <App></App>
        </BrowserRouter>
      </React.StrictMode>,
    )
    // 第三步：在app.js中使用useRoutes引入路由
    import {useRoutes} from 'react-router-dom'
    import router from './router/data'
    function App() {
      const outlet = useRoutes(router)
      return (
        <div className='App'>
          {outlet}
        </div>
      )
    }

    export default App

```

```js
    // ==========================旧的写法============================

    // 第一步：新建router/index.tsx文件
    import { BrowserRouter, Routes, Route } from "react-router-dom"
    import Test1 from "@/components/test1"
    import App from "@/App"
    const baseRouter = () => {
      return (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<App/>}>
              <Route path="/test1" element={<Test1/>}></Route>
            </Route>
          </Routes>
        </BrowserRouter>
      )
    }
    export default baseRouter

    // 第二步:在main.tsx文件中导入
    import React from 'react'
    import ReactDOM from 'react-dom/client'
    import 'reset-css'
    import '@/styles/global.scss'
    import Router from './router';

    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <Router></Router>
      </React.StrictMode>,
    )

    // 第三步：在app.tsx中添加路由展示区域占位符
    import {Outlet} from 'react-router-dom'

    function App() {
      return (
        <div className='App'>
          <Outlet></Outlet>
        </div>
      )
    }
    export default App

```