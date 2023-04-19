let people:{ name:string; age:number; say:() => void}
people = {
  name:'lisa',
  age:18,
  say: () => {
    console.log('say',)
  }
}
people.say()
let age = '18'
// function add (num1: number, num2:number){
//   return num2 + num1
// }
// const str = 'Hello'
// let p = {x: [10], y:() => {}}
// function formatPoint(point: typeof p){

// }
// formatPoint({x:10})
// let num: typeof p.y()
// class Person {
//   readonly age:number = 18
//   setAge () {
//     this.age = 20
//   }
//   constructor(age: number){
//     this.age = age
//   }
// }
