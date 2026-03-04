app.moduleB = (function () {
  var name = 'jisoo'
  var age = 20
  return {
    getName:function () {
      return name
    }
  }
})()
console.log(app.moduleA.getName())