import '../style.css'

// import { setupCounter } from './counter.js'
import { render } from './renderA'

render()

if(import.meta.hot){
  import.meta.hot.accept(['./renderA'],([
    newModuleA => {
      newModuleA.render()
    }
  ]))
}
// setupCounter(document.querySelector('#counter'))
