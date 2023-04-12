# watch失灵的几种情况
### (1)通过索引直接修改对应的值
```js
let arr = [45, 46, 47]
arr[1] = 12 // 监听不到变化
this.$set(arr, 1, 12) // 要改变的数组，索引，索引对应的值
```
### (2)修改数组的长度arr.length
```js
let arr = [45, 46, 47]
arr.length = 5
arr.splice(3, 2, [48, 49])
```
### (3)添加和修改对象的属性值
```js
let arr = [{
  name: '西游记'
},
{
  name: '三国演义'
}]
arr[1].show = true
let obj = arr[1]
obj.show = true
this.$set(arr, 1, obj) // 要改变的数组，索引，索引对应的值


let people = {name:'lisa',age: 25}
people.age = 20
this.$set( 'people', age , 20)
```
[!link]https://blog.csdn.net/qq_26780317/article/details/120130388