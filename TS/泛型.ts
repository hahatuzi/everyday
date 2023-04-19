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