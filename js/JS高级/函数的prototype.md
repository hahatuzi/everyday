# 函数的prototype属性：
1.每一个函数都存在一个prototype属性，它默认指向一个Object空对象（即称为：原型对象）,注意：是函数拥有一个prototype属性。
```js
console.log(typeof Date)// function
console.log(Date.prototype, typeof Date.prototype) // {}, Object
```
2.原型对象中有一个constructor属性，它指向函数对象本身。
```js
console.log(typeof Date)// function
console.log(Date.prototype.constructor) // Date()function
```
3.给函数的原型对象添加属性的作用：让函数的所有实例都自动拥有原型中的属性
```js
function Hello () {
    console.log('hello')
}
console.log(Hello.prototype)// {}
Hello.prototype.test = function () {
    console.log('test')
}
const num1 = new Hello()
console.log(num1.test)
```
4.应用场景：
可以用于将类似微信对象添加至vue原型对象上，从而可以在vue实例上调用微信对象的方法。
# 显式原型和隐式原型。
每一个函数都有一个prototype属性，被称为显式原型属性
每一个实例都有一个__proto__属性，被称为隐式原型，它指向它对应的构造函数的显式原型。
```js
function Hello () {
    console.log('hello')
}
console.log(Hello.prototype)// {}
const num1 = new Hello()
console.log(num1.__proto__)// {}
console.log(num1.__proto__ === Hello.prototype)
```
实例分析：
```js
function Fn() {
  this.test1 = function(){
    console.log('test1')
  }// this指向window，
}// 创建一个对象Fn
Fn.prototype.test2 = function(){
  console.log('test2')
}//在Fn的原型对象上创建一个属性test2
var fn = new Fn()
fn.test1()
fn.test2()
console.log(fn.toString())
fn.test3()
```