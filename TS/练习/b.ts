function  createArray<T> (length: number, value:  T ):T[] {
  let   result = []
  for(let i = 0; i < length; i++) {
      result[i] = value
  }
  return  result
}
console.log(createArray<string>(3, 'a'))
console.log(createArray<number>(3, 1))

let a:string | number
a = '123'
console.log(a.length)

a = 10
// console.log(a.length)


interface Deck{
  suits:string[];
  createCardPicker(this:Deck): () => object
}
let deck:Deck = {
  suits:['lisa','jisoo','jennie','rose'],
  createCardPicker:function (this:Deck){
    return () => {
      return this.suits.map(item => {
        suit:item
      })
    }
  }
}