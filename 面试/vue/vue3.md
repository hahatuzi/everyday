# 1.vue3的store工作流
 - store组成:state,getter,相当于computed,actions
 - store的使用：通过defineStore来定义一个store，包含了state和它的操作方式actions
 - pinia的使用：通过createPinia创建一个pinia,
 - store中的数据刷新后消失问题：通过'pinia-plugin-persistedstate'插件实现数据持久化，在store的属性中添加persist：true

# 2.vue2和vue3的区别
  - (1)双向绑定的方法不同，一个是Object.defineProperty,另一个是Proxy。
  - (2)v-if和v-for的优先级不同
  - (3)ref和$children不同

# vue3响应式原理
  vue3响应式原理 --> vue2原理 -->  两者对比 -->  proxy加reflect和Object.defineProperty
  源码结构 --> 打包方式，自定义打包脚本 --> monorepo架构
  reactive的实现