# 一：shallowRef和shallowReactive
  ### 1：shallowRef的应用场景，为什么有ref后还需要shallowRef呢？
   答：当创建一个**需要深层次更新属性的对象**时我们可以**使用ref**,但如果**仅关心浅层次或者最外层的变化**时我们可以**使用shallowRef**。
  ```js
    let sum = shallowRef(0)
    let person = shallowRef({
      name:"lisa",
      age:18
    })
    function changeSum () {
      sum.value += 10
    } // 更新成功
    function changePerson () {
      person.value = {name:'jisoo',age:19}
    } // 更新成功
    function changePersonName () {
      person.value.name = 'jinnie'
    } // 更新失败
  ```

  ### 2：shallowReactive的作用和shallowRef类似：
  仅会使对象的**最外层属性**变成响应式，不会对深层次的属性做任何处理，**避免了对每一个内部属性做响应式所带来的性能成本**。

  ### 3.triggerRef
  ```js
  import {triggerRef} from 'vue'
  let man = shallowRef({name:'lisa',props:{}})
  function change () {
    triggerRef(man)
  }
  ```
# 二：readonly和shallowReadonly
  ### 1：readonly
  **readonly**会让对象的**所有嵌套属性都变成只读的**。而**shallowReadonly**仅会使**最外层变成只读的**,内部深层次的还是可以改变的。
  ```js
    <div>
      <span>{{sum}}</span>
      <span>{{sum1}}</span>
    </div>
    let sum = ref(0)
    let sum1 = readonly(sum)
    let car = reactive({
      brand:'奔驰',
      attr:{
        color:'黑色'
      }
    })
    let car1 = shallowReadonly(car)
    let car2 = readonly(car)
    function changeSum () {
      sum.value += 1
    } // sum改变时sum1也会改变
    function changeSum1 () {
      sum1.value += 1
    } // sum1本身为只读，不可改变
    function changeCar () {
      car.brand = '宝马' // 修改car的时候car1也会变化
      car.attr.color = '蓝色'
    }
    function changeCar1 () {
      car1.brand = '宝马' // 最外层为只读属性
      car1.attr.color = '蓝色' // 深层次的属性可以修改
    }
  ```

# 三：toRaw和markRaw
  ### 1：toRaw用于获取响应式对象的原始对象，使用场景：toRaw尽量用于临时读取的场景,比如axios传参的时候
  ```js
    const person = {name:'lisa'}

    const reactivePerson = reactive(person)
    console.log(toRaw(reactivePerson) == person) // true
  ```
  ### 2：markRaw
  ```js
    let car = {brand:'奔驰',price:1000} // 原始对象
    let car1 = markRaw({brand:'奔驰',price:1000}) // car1标记为原始对象，无法变成响应式的
    let car2 = reactive(car) // 响应式
  ```


# 四：toRef和toRefs:
两个都是将响应式对象转化为普通对象，不同的是，**toRef仅转化某个属性**，**toRefs则是转化整个对象**
# 五:unref和isRef
unref：等同于val = isRef(val) ? val.value : val