function fn<T>(value:T):T{
  // console.log(value.length)
  return value
}
console.log(fn(2))
console.log(fn<string>('lisa')) // <string>可以省略
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
import _ from 'lodash'