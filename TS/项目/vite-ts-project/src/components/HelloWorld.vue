<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import type {ResData} from '../types/channels'

const props = defineProps<{ msg: string }>()
let _msg = ref(props.msg)
console.log(_msg)
const count = ref(0)
type Goods = {
  id:number,
  name:string
}
type Emits = {
  (e:'get-list', list:Goods[]):void
}
const emit = defineEmits<Emits>()
function handleClick () {
  count.value++
  emit('get-list',[{id:1,name:'lisa'}])
}
async function getList () {
  const data = axios.request<ResData>({
    url:'',
    method:'GET'
  })
}
</script>

<template>
  <div>
    <h1>{{ msg }}</h1>

    <div class="card">
      <button type="button" @click="handleClick">count is {{ count }}</button>
    </div>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
