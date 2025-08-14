import App from './App.vue'

import { createApp } from 'vue'
import './index.css'

const app = createApp(App)
console.log(app)
app.mount('#app')

function HelloWorld () {
  console.log('HelloWorld Rollup!!!')
  return Math.random(10).toString(16)
}

console.log('first', HelloWorld())
console.log('second', HelloWorld())

// 以下箭头函数会被转换为普通函数
const ES6Fn = () => {
  console.log('ok')
  return Math.random(10)
}
console.log(ES6Fn())
export {
  ES6Fn
}

// import {ref} from 'vue'
// var state = ref({
//   msg:'hello'
// })
// console.log(state)