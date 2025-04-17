// var a = require('commonMod1.js')
// console.log('a.name=', a.name)
// console.log('a.age=', a.getAge())

var name = 'lilei'
var age = 15
exports.name = name
exports.getAge = function () {
  return age
}

// (function(module, exports, require) {
//   // b.js
//   var a = require("a.js")
//   console.log('a.name=', a.name)
//   console.log('a.age=', a.getAge())

//   var name = 'lilei'
//   var age = 15
//   exports.name = name
//   exports.getAge = function () {
//     return age
//   }

// })(module, module.exports, require)

// bundle.js
// (function (modules) {
//   // 模块管理的实现
// })({
// 'a.js': function (module, exports, require) {
//   // a.js 文件内容
// },
// 'b.js': function (module, exports, require) {
//   // b.js 文件内容
// },
// 'index.js': function (module, exports, require) {
//   // index.js 文件内容
// }
// })