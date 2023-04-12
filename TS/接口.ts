// 接口用来定义一个类结构
(function () {
  interface myInterface {
    name:string;
    age:number
  }
  // 接口可以在定义类的时候去限制类的结构。
  const obj:myInterface = {
    name:'lisa',
    age:18
  }
})()