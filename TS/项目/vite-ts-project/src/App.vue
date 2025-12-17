<script setup lang="ts">
import './utils/updateData'
import {ref, reactive, computed, onMounted} from 'vue'
import HelloWorld from './components/HelloWorld.vue'
// const count = ref(100)
// console.log(count.value)
// const year = ref<number | string>(10)
// year.value = 'lisa'
type Good = {
  id:number,
  name:string,
  age:number
}
const goodList = ref<Good[]>([])
goodList.value = [
  {id:100, name:'lisa',age:18},
  {id:101, name:'jisoo',age:20},
]
type Form = {
  name:string,
  active?:boolean
}
const form:Form = reactive({
  name:'lisa'
})
form.active = false
type Address = {
  name:string,
  phone:string,
  gender?:'男' | '女'
}
const address:Address = reactive({
  name:'lisa',
  phone:'010-1112',
  gender:'女'
})
const count = ref(100)
const doubleCount = computed(() => {
  return count.value * 2
}) // 会自动进行类型推断
const newGoods = computed(() => {
  return goodList.value.filter(item => item.age > 18)
})
const inputChange = (e:Event) => {
  // 当change时间触发的时候，获取文本框中的数据
  console.log((e.target as HTMLInputElement).value)
}
const inputRef = ref<HTMLInputElement>(null)
onMounted(() => {
  inputRef.value?.focus() // 添加可选链，防止报错
})
function handleHello (e) {
  console.log(e)
}
</script>

<template>
  <div>
      {{goodList.map(item => {return item.id + '--' + item.name})}}
      <input type="text" @change="inputChange" ref="inputRef">
      <HelloWorld :msg="'title'" @getList="handleHello"></HelloWorld>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
