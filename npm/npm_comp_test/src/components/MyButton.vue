<template>
  <button>name-{{title}}</button>
</template>

<script>
export default {
  name:'MyButton',
  props:{
    title:{
      type:String,
      default: ''
    }
  }
}
</script>

<style>

</style>