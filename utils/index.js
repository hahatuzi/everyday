/**
* 参数处理
* @param {*} params  参数
*/
export function tansParams(params) {
  let result = ''
  for (const propName of Object.keys(params)) {
    const value = params[propName];
    var part = encodeURIComponent(propName) + "=";
    if (value !== null && value !== "" && typeof (value) !== "undefined") {
      if (typeof value === 'object') {
        for (const key of Object.keys(value)) {
          if (value[key] !== null && value[key] !== "" && typeof (value[key]) !== 'undefined') {
            let params = propName + '[' + key + ']';
            var subPart = encodeURIComponent(params) + "=";
            result += subPart + encodeURIComponent(value[key]) + "&";
          }
        }
      } else {
        result += part + encodeURIComponent(value) + "&";
      }
    }
  }
  return result
}

// 验证是否为blob格式
export function blobValidate(data) {
  return data.type !== 'application/json'
}
// 获取当前年月日
export function getToday (type = '-') {
  let year =  new Date().getFullYear()
  let month =  new Date().getMonth() + 1
  let date =  new Date().getDate()
  return year + type +  (month >= 10 ? month : '0' + month)  + type +  (date >= 10 ? date : '0' + date)
}

/**
* 是否滚动到页面底部
* @param {htmlELement} el  html元素
* @param {number} threshold  精度误差范围
*/
export function isAtBottom(el, threshold = 2) {
  const { scrollTop, scrollHeight, clientHeight } = el;
  return scrollHeight - scrollTop - clientHeight <= threshold;
}

/**
* 防抖
* @param {Function} fn  回调函数
* @param {number} delay  防抖时长
*/
export function throttle(fn, delay = 2000) {
  let timer = null;
  return function (...args) {
    if (timer) return;
    timer = setTimeout(() => {
      fn.apply(this, args);
      timer = null;
    }, delay);
  };
}