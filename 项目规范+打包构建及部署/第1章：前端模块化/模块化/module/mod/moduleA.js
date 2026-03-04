app.moduleA = (function () {
  var name = 'lisa'
  var age = 18
  return {
    getName:function () {
      return name
    }
  }
})()
console.log(app.moduleB.getName())
// 模块B可以取到模块A的东西，但模块A却取不到模块B的，因为上面这三个模块加载有先后顺序，互相依赖。当一个前端应用业务规模足够大后，这种依赖关系又变得异常难以维护。
