const name = 'jinne'
console.log('esm1')
import './esMod2'
// Uncaught SyntaxError: Unexpected token 'export' (at esMod2.js:1:1)
export {
  name
}