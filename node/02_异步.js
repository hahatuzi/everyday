function sum(a,b) {
  const begin = Date.now()
  while (Date.now() - begin < 10 * 1000) {
  }
  return a +b
}
console.log('1');
console.log(sum(1,3))
console.log('2')
