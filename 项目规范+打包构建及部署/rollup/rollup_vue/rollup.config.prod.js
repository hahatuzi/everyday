const babel = require('@rollup/plugin-babel')
const html = require('rollup-plugin-generate-html-template')
const resolve = require('@rollup/plugin-node-resolve')
// const terser = require('@rollup/plugin-terser')
module.exports = {
  input:'./src/index.js',
  output:{
    file:'dist/bundle.js',
    format:'esm',
    name:'MyModule' // 对外暴露的模块名称，仅在umd模式下生效
    // format:'iife'
  },
  plugins:[
    resolve(),
    babel({
      babelHelpers:'runtime',
      exclude: '/node_modules/**',
      extensions: ['.js', '.jsx', '.vue']
    }),
    html({
      template: './src/index.html',
      target: 'index.html',
      attrs:['type="module"'] // format为esm时需要添加attrs:['type="module"'] 
    }),
    // terser()
  ],
  // 排除项
  external:[]
}