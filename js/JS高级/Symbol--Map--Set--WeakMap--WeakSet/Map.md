# 
# 
```js
const map1 = new Map()
map1.set('a', 0)
```
# 实例方法：
```js
Map.prototype.clear() // 移除map对象中所有的键值对
Map.prototype.delete(key) // 移除指定键值对
Map.prototype.get(key) // 返回与key关联的值，若不存在，则返回undefined
Map.prototype.has(key) // 返回一个布尔值，用来表明Map对象中是否存在与key关联的值
Map.prototype.set(key, value) // 在Map对象中设置与指定的键key关联的 值value,并返回Map对象
Map.prototype.keys(), //返回一个迭代器对象，包含按照顺序插入的元素的key值
Map.prototype.values(), //返回一个迭代器对象，包含按照顺序插入的元素的values值
```
# Map的转化
  #### map转数组
  ```js
    let map = new Map([[1,'one'],[2,'two']])
    [...map.keys()]
    [...map.values()]
  ```
  #### 数组转map
  ```js
    let arr = [[1, 'one'],[2, 'two'],[3, 'three'],];
    let map = new Map(arr);
    console.log(map);
  ```
  #### map转对象
  ```js
  let map1 = new Map()
  map1.set('yes',true)
  map1.set('no',false)
  function mapToObj (map) {
    let obj = Object.create(null)
    for(let [key, value] of map) {
      obj[key] = value
    }
    return obj
  }
  console.log(mapToObj(map1))
  ```
  #### 对象转map,通过Object.entries()
  ```js
    let obj = {'yes':true, 'no':false}
    console.log(new Map(Object.entries(obj)))
  ```
  #### 对象转map,通过Object.entries()
  ```js
    let obj = {'yes':true, 'no':false}
    console.log(new Map(Object.entries(obj)))
  ```
  #### map转json
  ```js
  // map==>obj==>json
    function strMapToObj(strMap) {
          let obj = Object.create(null);//创建空的对象
          for (let [k, v] of strMap) {
              obj[k] = v;
          }
          return obj;
      }
      
      function strMapToJson(strMap) {
          return JSON.stringify(strMapToObj(strMap));
      }
  
      let myMap = new Map().set('yes', true).set('no', false);
      console.log(strMapToJson(myMap)); 
  // '{"yes":true,"no":false}'
  ```
# 例题
```js
// 1.
var arr = [3,3]
  var num = 9
  var map1 = new Map()
  var twoSum = function (source, target) {
    for (let index = 0; index < source.length; index++) {
      const data = target - source[index]
      if (map1.has(data)) {
        return [map1.get(data), index]
      } else {
        map1.set(source[index], index)
      }
    }
  }
  console.log(twoSum(arr, num))
// 2.
let arr = [{
  type:'类型一'
},{
  type:'类型二'
},{
  type:'类型三'
},{
  type:'类型一'
}]
let map1 = new Map()
arr.forEach((item,index) => {
  if (!map1.has(item.type)) {
    map1.set(item.type, index)
  }
})
console.log(map1)
console.log([...map2.keys()])
```