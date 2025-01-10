# watchEffect
### watchEffect：组件渲染时会立即执行一次,收集依赖，同时响应式的自动追踪其依赖，并在依赖更新的时候重新执行该函数
###　１.watch和watchEffect对比
（1）都可以监听响应式数据的变化，但是监听方式不同
（2）watch需要明确指出监听的数据
（3）watchEffect：不用明确指出监听的数据，函数中用到哪些属性，就是自动监听对应的属性
```js
let person = reactive({
  name:'lisa',
  age:20
})
watch([() => person.name,() => person.age], (newVal, oldVal) => {
  if(name == 'lisa' || age == 18){
    console.log('触发了')
  }
})
// watchEffect写法
watchEffect((newVal, oldVal) => {
  if(name == 'lisa' || age == 18){
    console.log('触发了') // 不写监听的是哪个属性， 当函数中用到的属性发生变化的时候会自动触发监听！！！
  }
})
```


watchEffect  --> 触发某数据的getter -->  getter中收集依赖 -->  修改该数据的时候触发setter  -->  setter中改变依赖