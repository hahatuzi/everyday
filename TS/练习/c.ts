class Animal {

  name:string;
  constructor(theName:string) {this.name = theName}
  move (distance:number) {
    console.log(`${this.name} moved ${distance}m`)
  }
}

class Dog extends Animal {
  constructor(name:string){super(name)}
  move( distance = 5){
    super.move(distance)
  }
}

let d1 = new Dog('d1')