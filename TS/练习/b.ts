function  createArray<T> (length: number, value:  T ):T[] {
  let   result = []
  for(let i = 0; i < length; i++) {
      result[i] = value
  }
  return  result
}
console.log(createArray<string>(3, 'a'))
console.log(createArray<number>(3, 1))