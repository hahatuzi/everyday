var people;
people = {
    name: 'lisa',
    age: 18,
    say: function () {
        console.log('say');
    }
};
people.say();
var age = '18';
// function add (num1: number, num2:number){
//   return num2 + num1
// }
// const str = 'Hello'
// let p = {x: [10], y:() => {}}
// function formatPoint(point: typeof p){
// }
// formatPoint({x:10})
// let num: typeof p.y()
// class Person {
//   readonly age:number = 18
//   setAge () {
//     this.age = 20
//   }
//   constructor(age: number){
//     this.age = age
//   }
// }
var Day;
(function (Day) {
    Day[Day["SUNDAY"] = 0] = "SUNDAY";
    Day[Day["MONDAY"] = 1] = "MONDAY";
    Day[Day["TUESDAY"] = 2] = "TUESDAY";
    Day[Day["WEDNESDAY"] = 3] = "WEDNESDAY";
    Day[Day["THUESDAY"] = 4] = "THUESDAY";
    Day[Day["FRIDAY"] = 5] = "FRIDAY";
    Day[Day["SATURDAY"] = 6] = "SATURDAY";
})(Day || (Day = {}));
console.log(Day.MONDAY);
// TS会为它们分配默认编号，从0开始
