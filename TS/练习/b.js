function createArray(length, value) {
    var result = [];
    for (var i = 0; i < length; i++) {
        result[i] = value;
    }
    return result;
}
console.log(createArray(3, 'a'));
console.log(createArray(3, 1));
var a;
a = '123';
console.log(a.length);
a = 10;
var deck = {
    suits: ['lisa', 'jisoo', 'jennie', 'rose'],
    createCardPicker: function () {
        var _this = this;
        return function () {
            return _this.suits.map(function (item) {
                suit: item;
            });
        };
    }
};
