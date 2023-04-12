class person {
  private _name:string;
  age:number;
  constructor(name:string,age:number) {
    this._name = name
    this.age = age
  };
  get name () {
    return this._name
  }
}
const per = new person('lisa', 18)
console.log(per.name)
console.log(per.age)