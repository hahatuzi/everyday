# computed的特性
  - 如果仅定义但是没有使用。那么computed内的方法不会触发
  - 缓存机制，多次调用computed定义的对象，但是computed内的函数没有改变时，也不会触发computed内的函数

```js
  let firstName = ref('张')
  let lastName = ref('三')
  let fullName = computed(() => {
    return firstName.value + '--' + lastName.value
  })
  function changeFullName () {
    fullName.value = '李四' // 会报错，因为value为只读属性，需要借助computed的get,set
  }

  let fullName1 = computed(() => {
    get () {
      return firstName.value + '--' + lastName.value
    },
    set (val) {
      const [str1, str2] = val.split('--')
      firstName.value = str1
      lastName.value = str2
    }
  })
```