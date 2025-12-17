# 导航守卫
  ```js
    import { useEffect } from 'react'
    import {useNavigate, useRoutes,useLocation } from 'react-router-dom'
    import routes from './router/data'
    import { message } from 'antd'

    function BeforeRouterEnter() {
      const outlet = useRoutes(routes)
      const token = localStorage.getItem('token')
      const navigateTo = useNavigate()
      const location = useLocation()
      // 登录页 && token  -->  to 首页
      // 非登录页 && 无token ----> to 登录页
      if (token) {
        if (location.pathname === '/login') {
          useEffect(() => {
            navigateTo('/home')
          },[])
        }
      } else {
        useEffect(() => {
          navigateTo('/login')
          message.error('请先登录')
        },[])
      }
      return outlet
    }

    function App() {
      return (
        <div className='App'>
          <BeforeRouterEnter></BeforeRouterEnter>
        </div>
      )
    }

    export default App
  ```
