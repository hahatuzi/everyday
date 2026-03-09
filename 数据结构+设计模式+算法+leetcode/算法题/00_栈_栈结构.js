function Stack() {
  // 栈的属性
  this.items = []
  // 栈的相关操作
  // push
  // this.push = function () {}方式一
  Stack.prototype.push = function (element) {
    this.items.push(element)
  }
  Stack.prototype.pop = function () {
    return this.items.pop()
  }
  Stack.prototype.peek = function () {
    return this.items[this.items.length - 1]
  }
  Stack.prototype.isEmpty = function () {
    return this.items.length == 0
  }
  Stack.prototype.size = function () {
    return this.items.length
  }
  Stack.prototype.toString = function () {
    return this.items.toString()
  }
}