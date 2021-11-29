function Observer (data) {
  this.data = data;
  this.walk(data);
}

Observer.prototype = {
  constructor: Observer,
  // this指向vm
  walk: function (data) {
    // this为observe的实例
    var me = this;
    Object.keys(data).forEach(function (key) {
      me.convert(key, data[key]);
    });
  },
  convert: function (key, val) {
    this.defineReactive(this.data, key, val);
  },

  defineReactive: function (data, key, val) {
    // 随着Observer的创建一起创建，而我们的Observer什么时候创建呢？new MVVM时创建Observer实例
    // 创建属性的dep对象
    var dep = new Dep();
    var childObj = observe(val);
    // data中的数据本身当然存在key，比如name:'lisa'的name属性名，但是并没有get和set方法，这也就是我们实现数据双向绑定的基础。
    Object.defineProperty(data, key, {
      enumerable: true, // 可枚举
      configurable: false, // 不能再define
      get: function () {
        // 建立dep和watcher的关系
        if (Dep.target) {
          dep.depend();
        }
        return val;
      },
      set: function (newVal) {
        if (newVal === val) {
          return;
        }
        val = newVal;
        // 新的值是object的话，进行监听
        childObj = observe(newVal);
        // 通知所有相关的订阅者watcher
        dep.notify();
      }
    });
  }
};
/*
* value:vm.data
*/
function observe (value, vm) {
  debugger
  // Observe递归结束条件
  if (!value || typeof value !== 'object') {
    return;
  }
  // 对data中的所有层级的对象递归遍历实现数据绑定
  // 如data:{
  // name:'lisa',
  //   subject:[{
  //     name:'english',
  //     teacher:'lili'
  //   }]
  // }
  return new Observer(value);
};


var uid = 0;

function Dep () {
  // 它的数量和Dep的执行次数一致，即data中的所有层级的对象递归遍历次数一致，所以它的个数和data中的属性对应
  this.id = uid++;
  this.subs = []; // 由订阅者组成的数组
}

Dep.prototype = {
  addSub: function (sub) {
    this.subs.push(sub);
  },
  // 建立dep和watcher的关系
  depend: function () {
    Dep.target.addDep(this);
  },

  removeSub: function (sub) {
    var index = this.subs.indexOf(sub);
    if (index != -1) {
      this.subs.splice(index, 1);
    }
  },

  notify: function () {
    this.subs.forEach(function (sub) {
      sub.update();
    });
  }
};

Dep.target = null;