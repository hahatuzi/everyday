// 函数通常包含两个参数global:全局变量,factory传递的函数
(function (global, factory ) {
  // 引出环境设置，该插件支持什么环境
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory() // 支持command.js标准，引入模块嗲嘛
  } else {
    if (typeof define == 'function' && define.amd) {
      define(factory)
    } else {
      // 浏览器模式
      global.Table = factory() // 在index.html文件中执行 <script src="./index.js"></script> <script>Table()</script>
    }
  }
})(this, function () {
  var Table = function () {
    console.log(123)
  }
  function isObject(obj){
    return typeof obj === 'object' && obj !== null
  }
  function isArray (arr) {
    return arr.constructor === Array
  }
  Table.init = function () {
    console.log('init')
  }
  Table.prototype.render = function () {
    console.log('render')
  }
  return Table
})