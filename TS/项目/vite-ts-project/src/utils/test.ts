export {}
let name:string = 'lisa'
// console.log(name)
let arr:number[] = [1,2,3]
arr.forEach(item => console.log(item.toFixed(2)))
// 联合类型
let arr1:(number | string)[] = [1,2,'a','b']
console.log(arr1)
type ItemType = (number | string)[]
let arr2:ItemType = [3,4,'d']
console.log(arr2)

let count:100
count = 200 //不能将类型“200”分配给类型“100”