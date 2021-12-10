/*
*自定义promise函数模块
*/
(function (window) {
  function Promise (excutor) {
    const _this = this
    this.status = 'pending'
    this.callbacks = []
    function resolve (value) {
      // 如果当前状态不是pending直接结束
      if (_this.status !== 'pending') return
      _this.status = 'fulfilled'
      _this.data = value
      // console.log('1', _this.callbacks)
      // 如果回调队列中有callback函数，立即异步执行回调函数
      if (_this.callbacks.length > 0) {
        setTimeout(() => {
          _this.callbacks.forEach(item => {
            item.onResolved(value)
          });
        })
      }
    }
    function reject (reason) {
      _this.status = 'rejected'
      _this.data = reason
      if (_this.callbacks.length > 0) {
        setTimeout(() => {
          _this.callbacks.forEach(item => {
            item.onRejected(reason)
          });
        })
      }
    }
    //  立即同步执行excutor
    try {
      excutor(resolve, reject)
    } catch (err) {
      // 如果执行器抛出异常，promise对象变成rejected状态
      reject(err)
    }
  }
  Promise.prototype = {
    // 指定成功的回调函数
    then: function (onResolved, onRejected) {
      onResolved = typeof onResolved === 'function' ? onResolved : value => value
      onRejected = typeof onRejected === 'function' ? onRejected : reason => { throw reason }
      return new Promise((resolve, reject) => {
        function handleStatus (callback) {
          try {
            const result = callback(this.data)
            // 回调函数结果是一个promise时，我们返回promise的结果
            if (result instanceof Promise) {
              // result.then(
              //   value => resolve(value),
              //   reason => reject(reason)
              // )
              result.then(resolve, reject)
              // 回调函数结果不是一个promise时，我们返回promise的结果
            } else {
              resolve(result)
            }
          } catch (error) {
            reject(error)
          }
        }
        // 假定当前的状态仍然是pending，此时先只是把函数放在回调队列中。需要等到状态改成fulfilled或者rejected后再执行回调函数
        if (this.status === 'pending') {
          // this.callbacks.push({
          //   onResolved,
          //   onRejected
          // })
          this.callbacks.push({
            onResolved (value) { handleStatus(onResolved) },
            onRejected (value) { handleStatus(onRejected) }
          })
        } else if (this.status === 'fulfilled') {
          setTimeout(() => {
            handleStatus(onResolved)
          })
        } else {
          setTimeout(() => {
            handleStatus(onRejected)
          })
        }
        // console.log('2')
      })

    },
    // 指定失败的回调函数
    // 返回值为一个新的promise对象
    catch: function (onRejected) {
      return this.then(undefined, onRejected)
    }
  }
  Promise.resolve = function (value) {

  }
  Promise.reject = function (reason) {

  }
  //返回一个promise，只有当所有promise都成功时才成功
  Promise.all = function (promises) {

  }
  Promise.race = function (promises) {

  }
  window.Promise = Promise
})(window)