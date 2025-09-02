const symbol1 = Symbol();
const symbol2 = Symbol(42);
const symbol3 = Symbol('foo');
console.log(symbol1) // Symbol()
console.log(symbol2) // Symbol()
console.log(symbol3) // Symbol()
// =======类型判断============
let a = Symbol('age')
console.log(typeof a) // symbol
// =====作为属性名===
let obj = {}
let prop1 = Symbol('age')
let prop2 = 'age'
obj[prop1] = 18
obj[prop2] = 20
console.log(obj) // {age: 20, Symbol(age): 18}
console.log(obj[prop1]) // 18
console.log(obj.prop1) // undefined,symbol定义的属性名无法通过.获取属性值
// ==============遍历对象============
console.log(Object.keys(obj)) // ['age']
console.log(Object.getOwnPropertyNames(obj)) // ['age']
console.log(Object.getOwnPropertySymbols(obj)) // [Symbol(age)]
for (const key in obj) {
  console.log(key) // 'age'
}
console.log(Reflect.ownKeys())
let SymbolArr = Object.getOwnPropertySymbols(obj)
for (const element of SymbolArr) {
  console.log(element,'---',obj[element])  // Symbol(age)---18
}
// ============创建相同的symbol==========
const s1 = Symbol.for('aaa')
const s2 = Symbol.for('aaa')
console.log(typeof s1, typeof s2) // symbol, symbol
console.log(s1 === s2) // true
// ============创建不同的symbol===============
const s3 = Symbol('bbb')
const s4 = Symbol('bbb')
console.log(typeof s3, typeof s4) // symbol, symbol
console.log(s3 === s4) // false

// symbol.for
let key1 = Symbol.keyFor(s1)
console.log(key1) // aaa
let key2 = Symbol.keyFor(s2)
console.log(key1 === key2) // true