# call
```js
  function Person (name, age) {
    this.name = name
    this.age = age
  }
  function Student (name, age, price) {
    Person.call(this, name, age) // this.Person(name, age)
    this.price = price
  }
```