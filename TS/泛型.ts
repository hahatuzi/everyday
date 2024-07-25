function fn<T>(value:T):T{
  // console.log(value.length)
  return value
}
console.log(fn(2))
console.log(fn<string>('lisa')) // <string>可以省略

// 泛型定义：
interface ILength {
  length: number
}
function fn1<T extends ILength>(value: T): T{
  console.log(value.length)
  return value
}
console.log(fn1('lisa'))
type PropsKeys = 'x' | 'y' | 'z' | 'a' 

// partical<Type>的实现
type Partical<T> = {
  [P in keyof T]?: T[P]
}
type  Props = {a:number; b:string; c:boolean}
type type3 = Props['a']
type type4 = Props['a' | 'b']
type type5 = Props[keyof Props]
// import _ from 'lodash'


interface Data1 {
  name:string,
  age:number
}
interface Data2 {
  type:string,
  id:number
}
interface Res<T> {
  code:number,
  msg:string,
  data:T
}
let res1:Res<Data1> = {
  code:200,
  msg:'接口调用成功',
  data:{
    name:'lisa',
    age:18
  }
}