<template>
  <div>Hello-{{title}}</div>
</template>

<script>
export default {
  name: 'HelloWorld',
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