# effect作用域，可以补货其中所创建的响应式副作用（计算属性和侦听器）
  ```js
    let {reactive, effect} = Vue
    let state = reactive({name:'lisa',age:18})
    effect(() => {
      app.innerHTML = state.name + state.age
    },{
      lazy:true // 懒加载，不会触发更新
    })
    setTimeout(() => {
      state.name = 'jisoo'
    },1000)
    // effect可以触发get收集effect,也可以触发set执行effect,相当于watch
  ```