function fibonacci (n) {
  return n <= 2 ? 1 : fibonacci(n - 1) + fibonacci(n - 2)
}

var onmessage = function (e) {
  var number = e.data
  console.log('分线程',number)
  var result = fibonacci(number)
  postMessage(result)
}