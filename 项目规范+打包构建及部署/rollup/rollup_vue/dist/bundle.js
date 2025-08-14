import { createElementBlock, openBlock, toDisplayString, createApp } from 'vue';

var script = {
  data: function data() {
    return {
      title: 'hello vue!!!'
    };
  }
};

function render(_ctx, _cache, $props, $setup, $data, $options) {
  return openBlock(), createElementBlock("div", null, toDisplayString($data.title), 1 /* TEXT */);
}

script.render = render;
script.__file = "src/App.vue";

var app = createApp(script);
console.log(app);
app.mount('#app');
function HelloWorld() {
  console.log('HelloWorld Rollup!!!');
  return Math.random(10).toString(16);
}
console.log('first', HelloWorld());
console.log('second', HelloWorld());

// 以下箭头函数会被转换为普通函数
var ES6Fn = function ES6Fn() {
  console.log('ok');
  return Math.random(10);
};
console.log(ES6Fn());

// import {ref} from 'vue'
// var state = ref({
//   msg:'hello'
// })
// console.log(state)

export { ES6Fn };
