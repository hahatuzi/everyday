var person = /** @class */ (function () {
    function person(name, age) {
        this._name = name;
        this.age = age;
    }
    ;
    Object.defineProperty(person.prototype, "name", {
        get: function () {
            return this._name;
        },
        enumerable: false,
        configurable: true
    });
    return person;
}());
var per = new person('lisa', 18);
console.log(per.name);
console.log(per.age);
