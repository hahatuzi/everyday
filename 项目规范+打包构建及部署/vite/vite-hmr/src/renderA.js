import javascriptLogo from '../javascript.svg'
import viteLogo from '/vite.svg'

let index = import.meta.hot.data.index || 0
let timer;
export function render () {
  timer = setInterval(() => {
    index++
    document.querySelector('#app').innerHTML = `
    <div>
      <a href="https://vitejs.dev" target="_blank">
        <img src="${viteLogo}" class="logo" alt="Vite logo" />
      </a>
      <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
        <img src="${javascriptLogo}" class="logo vanilla" alt="JavaScript logo" />
      </a>
      <h1>Hello Vite!!!${index}</h1>
      <div class="card">
        <button id="counter" type="button"></button>
      </div>
      <p class="read-the-docs">
        Click on the Vite logo to learn more
      </p>
    </div>
  `}, 1000)
}


if(import.meta.hot) {
  // import.meta.hot.accept()
  import.meta.hot.data.index = index
  console.log(import.meta.hot.data);
  import.meta.hot.dispose(() => {
    clearInterval(timer)
  })
}