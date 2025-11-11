# props的相关信息
  ### 1.props的children属性
  ### 2.props校验
    ```js
      // 使用步骤
      // 1.安装包 prop-types
      // 2.导入prop-types
      // 3.使用组件名.propTypes = {} 来给组件的props添加校验规则
      import PropsTypes from 'prop-types'
      function App (props) {
        return (
          <div>Hello world！{props.colors}</div>
        )
      }
      App.propTypes = {
        colors:PropTypes.array //约定colors为array类型，如果类型不对，则报错用于分析原因
      }
      // propTypes的常见约束类型：
      // array,bool,number, func, object,strnig,
      // element(React元素类型)，
      // isrequired(必填项)，
      // 特定结构的类型
      // propTypes.shape({name:string,age:number})
    ```
  ### 3.props的默认值
    ```js
      function App(props){
        return (
          <div>{props.pageSize}</div>
        )
      }
      App.defaultProps = {
        pageSize:20
      }
    ```