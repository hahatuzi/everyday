# reduce()哇噻这个方法的参数实在是太多了,我们来分析一下它。
```js
/*
* 参数一：callback(形参一，形参二，形参三，形参四)函数
*        //形参一：accumulator,初时数据由参数二accumulatorInitialValue提供，注：如果没有提供初始值，则将使用数组中的第一个元素。 在没有初始值的空数组上调用 reduce 将报错。
*        //形参二：currentValue，数组正在处理的元素
*        //形参三：index，数组正在处理的元素的索引，注：如果提供了参数二，index初始值就是0，否则就是1
*        //形参四：sourceArray，源数组，调用reduce的数组。
* 参数二：accumulatorInitialValue，作为参数一callback()的第一个形式参数,注：如果没有提供初始值，则将使用数组中的第一个元素。 在没有初始值的空数组上调用 reduce 将报错。
*/
arr.reduce(callback(accumulator, currentValue,index,sourceArray),accumulatorInitialValue)
// callback()的执行次数为数组长度
```
# 应用场景：
1.数组去重
```js
let arr = ['a', 'b', 'a', 'b', 'c', 'e', 'e', 'c', 'd', 'd', 'd', 'd']
var res = arr.reduce(function (result, item, index) {
  if (result.indexOf(item) === -1) {
    result.push(item)
  }
  return result
}, [])
console.log(res)
// 发散：去重的话我们只需要结合循环和indexOf判断即可，所以像forEach,map等均可。
```
2.数组求和
```js
var sum = [1,42,3,5].reduce((res,item)=>{
  res += item
  return res
},0)
```
3.二维数组转一维
```js
var result = [[1,2],[3,4]].reduce((res,item)=>{
  return res.concat(item)
},[])
```