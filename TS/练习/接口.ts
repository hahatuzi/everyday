// 接口用来定义一个类结构
(function () {
  interface myInterface {
    name:string;
    age:number
  }
  // 接口可以在定义类的时候去限制类的结构。
  const obj:myInterface = {
    name:'lisa',
    age:18
  }
})()
interface Point2D {
  x:number
}
interface Point3D {
  x:number
  y:number
}
let p3: Point2D
// class  Point4D {
//   z:number
// }
// let p4:Point4D = new Point4D()
interface Per {name: String}
interface Contact {phone: String}
type PersonContact = Per & Contact
let obj:PersonContact = {
  name: 'lisa',
  phone: '181'
}
interface A{
  fn:(value: number) => string
}
// interface B extends A{
//   fn:(value: string) => string
// }
interface B{
  fn:(value: string) => string
}
type CC = A & B
// let cc: CC = {
//   fn(value: number | string) {
//    return ''
//   }
// }
let cc:CC
// cc.fn(1)

interface Shape{
  color:string
}
interface PenStroke{
  size:string
}
interface Square extends Shape,PenStroke{
  name:string
}
let s1 = <Square>{}
s1.color = '#fff'
s1.size = 'small'
s1.name = 'lisa'

// typeof的使用
// interface IPerson {
//   name:string;
//   age:number
// }
// 当接口有初始变量的时候可以采用改方式
const person = {
  name:'张三',
  age:18
}
type IPerson = typeof person