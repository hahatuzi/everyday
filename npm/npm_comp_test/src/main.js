import Vue from 'vue'
import App from './App.vue'
import npm_comp_test from 'npm_comp_test'
Vue.config.productionTip = false
Vue.use(npm_comp_test)
new Vue({
  render: h => h(App),
}).$mount('#app')
