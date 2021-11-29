function Compile (el, vm) {
  console.log(el, vm)
  // 保存vm到compile对象
  this.$vm = vm;
  // 如果有el属性，即有绑定元素
  this.$el = this.isElementNode(el) ? el : document.querySelector(el);

  if (this.$el) {
    // nodeToFragment，1.取出el元素中的所有子节点保存到一个fragment对象中。
    this.$fragment = this.node2Fragment(this.$el);
    // 2.编译fragment中的所有层次子节点
    this.init();
    // 3.将编译好的fragment添加到页面的el元素中。
    this.$el.appendChild(this.$fragment);
  }
}

Compile.prototype = {
  constructor: Compile,
  node2Fragment: function (el) {
    // 创建空的fragment对象
    var fragment = document.createDocumentFragment(),
      child;

    // 将原生节点拷贝到fragment
    while (child = el.firstChild) {
      fragment.appendChild(child);
    }

    return fragment;
  },
  // 将🈯️定元素/fragment对象进行编译
  init: function () {
    this.compileElement(this.$fragment);
  },

  compileElement: function (el) {
    var childNodes = el.childNodes,
      me = this;
    // 遍历元素子节点，伪数组转换为数组。
    [].slice.call(childNodes).forEach(function (node) {
      var text = node.textContent;
      var reg = /\{\{(.*)\}\}/;
      // 元素节点 nodeType = 1
      if (me.isElementNode(node)) {
        me.compile(node);

      } else if (me.isTextNode(node) && reg.test(text)) {
        me.compileText(node, RegExp.$1.trim());
      }

      if (node.childNodes && node.childNodes.length) {
        me.compileElement(node);
      }
    });
  },

  compile: function (node) {
    // 获取到所有元素节点
    var nodeAttrs = node.attributes,
      me = this;
    [].slice.call(nodeAttrs).forEach(function (attr) {
      // 获取属性名
      var attrName = attr.name;
      // 从属性名中获取到指令名
      if (me.isDirective(attrName)) {
        var exp = attr.value;
        var dir = attrName.substring(2);
        // 事件指令
        if (me.isEventDirective(dir)) {
          compileUtil.eventHandler(node, me.$vm, exp, dir);
          // 普通指令
        } else {
          compileUtil[dir] && compileUtil[dir](node, me.$vm, exp);
        }

        node.removeAttribute(attrName);
      }
    });
  },

  compileText: function (node, exp) {
    compileUtil.text(node, this.$vm, exp);
  },

  isDirective: function (attr) {
    return attr.indexOf('v-') == 0;
  },

  isEventDirective: function (dir) {
    return dir.indexOf('on') === 0;
  },

  isElementNode: function (node) {
    return node.nodeType == 1;
  },

  isTextNode: function (node) {
    return node.nodeType == 3;
  }
};

// 指令处理集合
var compileUtil = {
  // 解析v-text/{{}}
  text: function (node, vm, exp) {
    this.bind(node, vm, exp, 'text');
  },
  // 解析v-html
  html: function (node, vm, exp) {
    this.bind(node, vm, exp, 'html');
  },
  // 解析v-model
  model: function (node, vm, exp) {
    this.bind(node, vm, exp, 'model');

    var me = this,
      val = this._getVMVal(vm, exp);
    node.addEventListener('input', function (e) {
      var newValue = e.target.value;
      if (val === newValue) {
        return;
      }

      me._setVMVal(vm, exp, newValue);
      val = newValue;
    });
  },
  // 解析v-model
  class: function (node, vm, exp) {
    this.bind(node, vm, exp, 'class');
  },
  // 解析v-bind
  bind: function (node, vm, exp, dir) {
    var updaterFn = updater[dir + 'Updater'];
    // 调用函数更新节点， 如textUpdater(),htmlUpdater()
    // 当我们在此获取到属性的值时会嗲用object.get方法,从而
    updaterFn && updaterFn(node, this._getVMVal(vm, exp));
    // 当表达式对应的属性发生变化时执行，如上面中的text中的{{}}，用来更新显示数据
    new Watcher(vm, exp, function (value, oldValue) {
      updaterFn && updaterFn(node, value, oldValue);
    });
  },

  // 事件处理
  eventHandler: function (node, vm, exp, dir) {
    var eventType = dir.split(':')[1],
      fn = vm.$options.methods && vm.$options.methods[exp];

    if (eventType && fn) {
      // 目的在于给标签绑定事件监听
      // bind返回新的函数，且强制绑定新的对象vm,
      node.addEventListener(eventType, fn.bind(vm), false);
    }
  },
  // 从vmh中得到表达式对应的值
  _getVMVal: function (vm, exp) {
    var val = vm;
    exp = exp.split('.');
    exp.forEach(function (k) {
      val = val[k];
    });
    return val;
  },

  _setVMVal: function (vm, exp, value) {
    var val = vm;
    exp = exp.split('.');
    exp.forEach(function (k, i) {
      // 非最后一个key，更新val的值
      if (i < exp.length - 1) {
        val = val[k];
      } else {
        val[k] = value;
      }
    });
  }
};

// 更新器,包含多个更新节点的方法的工具对象
var updater = {
  // 更新节点的textContent属性值
  textUpdater: function (node, value) {
    node.textContent = typeof value == 'undefined' ? '' : value;
  },
  // 更新节点的innerHTML属性值
  htmlUpdater: function (node, value) {
    node.innerHTML = typeof value == 'undefined' ? '' : value;
  },
  // 更新节点的className属性值
  classUpdater: function (node, value, oldValue) {
    var className = node.className;
    className = className.replace(oldValue, '').replace(/\s$/, '');

    var space = className && String(value) ? ' ' : '';

    node.className = className + space + value;
  },
  // 更新节点的value属性值
  modelUpdater: function (node, value, oldValue) {
    node.value = typeof value == 'undefined' ? '' : value;
  }
};

// read.me
// 模板解析主要包括两部分：
// （1）大括号表达式解析：获取到文本节点textNode并正则匹配{{ }}  ---> 从vmH中取出{{ }}的内容name对应的属性值， --->  将该值插入该文本节点textNode内部
// （2）事件指令解析：获取到元素节点ElementNode --->  获取到元素节点的属性attr --->  截取到属性的名称 --->  判断该属性是否为事件属性还是一般指令 --->  取出该属性的值，再从vmH中取出methods中该属性值对应的方法 --->  向Node上addEventListener
// （3）一般指令解析