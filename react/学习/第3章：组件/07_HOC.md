# 一：基本语法：
  - 1.创建一个函数，名称约定以with开头
  - 2.指定函数参数，参数应该以大写字母开头
  - 3.在函数内部创建一个类组件，提供复用的状态逻辑
  - 4.在该组件中，渲染参数组件，同时将状态通过props传递给参数组件
  ```js
    function  withMouse(WrapperComponent) {
      class  Mouse  extends  React.Component()
      return  Mouse
    }
    // Mouse组件内的render方法：
    return     <wrapperComponent   {...this.state}></WrapperComponent>
  ```

  ```js
    function withSubscription (wrapComponent) {
      class APP extends React.component {


        render () {
          return <wrapComponent/>
        }
      }
    }
  ```