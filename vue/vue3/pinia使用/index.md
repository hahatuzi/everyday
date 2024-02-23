# 使用流程
### 一：store文件夹--index.js文件
  ```js
  import { createPinia } from "pinia";
  const pinia = createPinia()
  export default pinia
  ```
### 二：store文件夹--user文件
  ```js
  // 
  // 用户信息
  import { defineStore } from 'pinia'
  import {constantRoute} from '@/router/index'
  const useUserStore = defineStore('user', {
    state: () => {
      return {
        userName:'',
        token: localStorage.getItem('token'),
        menuRoutes: constantRoute // 菜单路由数组
      }
    },
    actions:{
      userLogin(form){
        this.userName = form.name
        console.log('userLogin',this.userName)
        this.token = form.token
      }
    },
    getters:{}
  })
  export default useUserStore
  ```
### 三：页面使用
  ```js
  import useUserStore from '@/store/modules/user'
  const userStore = useUserStore()
  ```