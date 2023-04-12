let people:{ name:string; age:number; say:() => void}
people = {
  name:'lisa',
  age:18,
  say: () => {
    console.log('say',)
  }
}
people.say()