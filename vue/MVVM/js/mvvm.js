/*
*/
function MVVM (options) {
  this.$options = options || {}; // 将配置对象保存到实例vmH中
  var data = this._data = this.$options.data; // 将vmH的配置对象做一份保存记录到vmH的_data属性上。
  var me = this; // this指向实例对象vmH

  // 数据代理，对指定的属性进行代理
  // 实现 vm.xxx -> vm._data.xxx
  Object.keys(data).forEach(function (key) {
    me._proxyData(key);
  });

  this._initComputed();

  observe(data, this);

  this.$compile = new Compile(options.el || document.body, this)
}

MVVM.prototype = {
  constructor: MVVM,
  $watch: function (key, cb, options) {
    new Watcher(this, key, cb);
  },
  /*
  *  指定属性代理的实现方法
  * key：属性名
  */
  _proxyData: function (key, setter, getter) {
    var me = this; // 保存实例对象vmH
    setter = setter ||
      // 给vmH添加key属性名对应的属性值
      Object.defineProperty(me, key, {
        configurable: false,
        enumerable: true,
        // 当通过vm.XX读取属性值时调用，从data中获取对应的属性值返回
        get: function proxyGetter () {
          return me._data[key];
        },
        // 当通过vm.xxx = value时，value被保存到data对应的属性上
        set: function proxySetter (newVal) {
          console.log(me)
          me._data[key] = newVal;
          console.log(me)
        }
      });
  },

  _initComputed: function () {
    var me = this;
    var computed = this.$options.computed;
    if (typeof computed === 'object') {
      Object.keys(computed).forEach(function (key) {
        Object.defineProperty(me, key, {
          get: typeof computed[key] === 'function'
            ? computed[key]
            : computed[key].get,
          set: function () { }
        });
      });
    }
  }
};

Object.defineProperty({ name: 'lisa' }, getter, se)