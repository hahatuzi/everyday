# 一：创建方式
  - 1.使用CRA创建支持TS的项目
    ```js
      npx  create-react-app 项目名称 --template  typescript
    ```

# 二：tsconfig.json
  ```js
    {
      "exclude": [
        "练习/app.ts"
      ],
      "compilerOptions": {
        "allowJs": false, // 是否对js进行编译
        "checkJs": false, // 检查js语法是否符合规范
        "skipLibCheck": false, // 是否跳过声明文件的类型检查
        "removeComments": false, // 是否移除注释
        "noEmitOnError": true, // 当发生错误时不允许生成编译文件
        "noImplicitAny": true, // 不允许隐式的any类型
        "strictNullChecks": false, // 不允许把null,undefiners赋值给其他类型
        "strict": true, // 所有严格检查的总开关
        "alwaysStrict": false // 用来设置编译后的文件是否使用严格模式
      }
    }
  ```

# 三：react-app-env.d.ts：它是React的默认的类型声明文件
  ### 1.**三斜线指令**：指定依赖的其他类型声明文件，types表示依赖的类型声明文件包的名称。解释：告诉TS帮我们加载react-scripts这个包提供的类型声明
  ### 2.react-scripts的类型声明文件包含了两部分类型
  - （1）react,rect-dom,node的类型
  - （2）图片样式等模块的类型，以允许在代码中导入图片，svg等文件

# 四： 使用
  ### 1.函数
    ```js
      // 函数组件类型
      type Props = { name: string; age?: number }
      const Hello:FC<Props> = ({ name,age }) => (
        <div>我的名字叫{name},年龄{age}</div>
      )
      // 上述写法可以简化为：
      const  Hello = ({ name, age }:Props) => (
        <div>我的名字叫{name},年龄{age}</div>
      )
    ```

  ### 2.类组件
  - (1)定义组件类型
    ```js
      // 无props和state
      class  C1 extends React.Component {}
      // 有props无state
      class C2  extends React.Component<Props> {}
      // 无props有state
      class  C3 extends React.Component <{}, State> {}
      // 有props和state
      class  C4 extends  React.Component <Props, state> {}
    ```

  - (2)属性和属性默认值
    ```js
      type  Props = { name: string; age?: number };
      class  Hello  extends  React.Component<Props> {
        static  defaultProps: Partial<Props> = {
          age: 18
        };
        render () {
          const  { name,age  } = this.props
          return <div>my  name is {name}, age {age}<div>
        }
      }
    ```
  - (3)状态和事件
    ```js
      type  State = { count: number }
      class  Counter  extends  React.Component<{}, State> {
        state: State = {
            count: 0
        }
        onAdd = （） => {
          count: this.state.count + 1
        }
        return (
        <div>
            <button onClick={this.onAdd}>+1</button>
        </div>
        )
      }
    ```