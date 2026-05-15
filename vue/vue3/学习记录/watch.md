侦听器 data 源可以是返回值的 getter 函数，也可以是 ref：

# 情况一：监听ref定义的基本数据类型
  直接写变量名即可，监听的是它value值得改变
  ```js
    let sum = ref(0)
    // 监听ref定义的基本数据类型,直接写变量名
    const stopWatch = watch(sum, (newVal, oldVal) => {
        console.log(newVal, oldVal)
        if ( newVal  >= 10) {
            stopWatch()  //   stopWatch:watch()用于解除监听
        }
    })
  ```

# 情况二：监听ref定义的对象类型
  直接写变量名，**监听的是对象的地址值**,**newVal和oldVal指向不同的地址值**，非同一个对象。监听**对象内部的数据**时需要**开启deep**。
  ```js
    let person = ref({
      name:'张三',
      age:18
    })
    // 监听ref定义的对象类型,直接写变量名
    watch(person, (newVal,oldVal) => {
      console.log(newVal,oldVal) //newVal和oldVal指向不同的地址值
    })
    function change () {
      person.value = {name:'lisa'}
    }
  ```

# 情况三：监听reactive定义的对象类型的数据，
此时是**默认已经开启了深度监视**的,无需再使用deep：true
```js
  watch(person, (newVal,oldVal) => {
    console.log(newVal,oldVal)
  })
```


### (4)监听响应式对象中的某个属性,通常改属性分为两种情况：基本类型，对象类型。基本类型要写成函数式，对象类型可以直接写也可以写成函数式
```js
let person = reactive({
  name:'lisa',
  obj:{
    o1:'o1',
    o2:'o2'
  },
  children:[{
    name:'lisa-1'
  }]
})
// 
watch(() => person.name, (newVal,oldVal) => {
  console.log(newVal,oldVal)
})
```