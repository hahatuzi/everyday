app.mod2 = {}
app.mod2.name = 'hanmeimei'
app.mod2.age = 13
app.mod2.name = 'lisa'
// b.js 模块的开发者，可以很方便的通过 app.moduleA.name 来取到模块A中的名字，但是也可以通过 app.moduleA.name = 'rename' 来任意改掉模块A中的名字，而这件事情，模块A却毫不知情！这显然是不被允许的。
console.log(app)