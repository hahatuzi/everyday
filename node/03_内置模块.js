setTimeout(() => {
  console.log(1);
  
}, 0);

queueMicrotask(()=>{
  console.log(2);
  
})
process.nextTick(()=>{
  console.log(3);
  
})
console.log(4);
// 4,3,2,1