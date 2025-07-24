class MVVM {
  constructor(el, data) {
    this.el = document.querySelector(el)
    this._data = data
    this.init()
  }
  init () {
    this.initData()
  }
  initData () {
    const _this = this
    this.data = {}
    for (const key in this._data) {
      Object.defineProperty(this.data, key, {
        get () {
          return _this._data[key]
        },
        set(newValue){
          _this._data[key] = newValue
        }
      })
    }
    console.log(this.data)
  }
  bindInput (el) {
    const _allInputs = el.querySelectorAll('input')
    _allInputs.forEach(input => {
      
    })
  }
}