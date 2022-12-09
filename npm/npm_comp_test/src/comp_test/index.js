import HelloWorld from '../components/HelloWorld.vue'
import MyButton from '../components/MyButton.vue'
const install = (Vue) => {
  Vue.component(HelloWorld.name, HelloWorld)
  Vue.component(MyButton.name, MyButton)
}
export default install