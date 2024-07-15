# 使用流程
### 一：store文件夹--index.js文件
  ```js
  import { createPinia } from "pinia";
  import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate) // 该插件配合以下的persist来实现数据的持久性

  export default pinia
  ```
### 二：store文件夹--user文件
  ```js
  // 
  // 用户信息
  import { defineStore } from 'pinia'
  import {constantRoute} from '@/router/index'
  const useUserStore = defineStore('user', {
    persist:true // persist用来实现数据持久性
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
    getters:{
      newName (state){
        return '王' + state.userName
      }
    }
  })
  export default useUserStore
  // 可以将state视为商店的data，将getters视为商店的computed属性，将actions视为methods
  ```
### 三：页面使用
  ```js
  import useUserStore from '@/store/modules/user'
  const userStore = useUserStore()
  // 使用storeToRefs(userStore)来获取store内的数据，storeToRefs不会对方法进行ref包裹
  const{userName} = storeToRefs(userStore)
  // 使用$subscribe来监听store中数据的更新，并根据监听来进行一些操作
  userStore.$subscribe((mutate,state) => {
    console.log('update',mutate,state)
  })
  ```