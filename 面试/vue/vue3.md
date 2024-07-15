# 1.vue3的store工作流
 - store组成:state,getter,相当于computed,actions
 - store的使用：通过defineStore来定义一个store，包含了state和它的操作方式actions
 - pinia的使用：通过createPinia创建一个pinia,
 - store中的数据刷新后消失问题：通过'pinia-plugin-persistedstate'插件实现数据持久化，在store的属性中添加persist：true