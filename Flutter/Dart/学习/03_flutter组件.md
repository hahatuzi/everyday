# 一：基础组件--MaterialApp
  整个应用都被MaterialApp包裹，方便对整个应用进行整体风格设计
  ### 1.属性介绍：title,theme,home
  - **title**:用来展示窗口的标题内容
  - **theme**：用来设置整个应用的主题
  - **home**:用来展示窗口的主体内容

# 二：基础组件
  ### 1.scaffold：用于构建Material Design风格页面的核心布局组件，提供标准，灵活配置的页面骨架
  ### 2.Container用来作为容器，设置高度用height属性,child属性用来存放子组件
  ### 3.Text是用来显示文本的组件
    ```js
      void main () {
        runApp(
          title:"Hello Flutter",
          theme: ThemeData(scaffoldBackgroundColor: Colors.blue),
          home: Scaffold(
            appBar:AppBar(
              title:Text('头部区域')
            ),
            body:Container(
              child:Center(
                child:Text('中间区域')
              )
            ),
            bottomNavigationBar:Container(
              height:80,
              child:Center(
                child:Text('底部区域')
              )
            )
          )
        )
      }
    ```

# 三：Flutter自定义组件：无状态组件和有状态组件
  ### 1.无状态组件StatelessWidget
    ```js
      void main() {
        runApp(MainPage());
      }

      class MainPage extends StatelessWidget {
        @override
        Widget build(BuildContext context) {
          return MaterialApp(
          title:"Hello Flutter",
          theme: ThemeData(scaffoldBackgroundColor: Colors.blue),
          home: Scaffold(
            appBar:AppBar(
              title:Text('头部区域')
            ),
            body:Container(
              child:Center(
                child:Text('中间区域')
              )
            ),
            bottomNavigationBar:Container(
              height:80,
              child:Center(
                child:Text('底部区域')
              )
            )
          )
        );
        }
      }
    ```
  ### 2.有状态组件StatefulWidget
  - 有状态组件是构建动态交互界面的核心，当**状态改变**时，组件会更新显示内容
  - 第一步：创建两个类，第一个类继承StatefulWidget类，主要接收和定义最终参数，核心作用是创建State对象
  - 第二个类继承State<第一个类名>，负责管理所有可变的数据和业务逻辑，并实现build构建方法，build方法需要返回一个widget
    ```js
      void main() {
        runApp(MainPage());
      }
      // 第一个类：对外，继承StatefulWidget类
      class MainPage extends StatefulWidget {
        @override
        State<StatefulWidget> createState() {
          // TODO: implement createState
          // return 第二个类的对象
          return _MainPageState();
          // throw UnimplementedError();
        }
      }
      // 第二个类：内部类，负责管理数据，处理业务逻辑，并且渲染视图
      class _MainPageState extends State<MainPage> {
        @override
        Widget build(BuildContext context) {
          return MaterialApp(
          title:"Hello Flutter",
          theme: ThemeData(scaffoldBackgroundColor: Colors.blue),
          home: Scaffold(
            appBar:AppBar(
              title:Text('有状态组件--头部区域')
            ),
            body:Container(
              child:Center(
                child:Text('中间区域')
              )
            ),
            bottomNavigationBar:Container(
              height:80,
              child:Center(
                child:Text('底部区域')
              )
            )
          )
        );
        }
      }
    ```
  ### 3.无状态组件的生命周期
    - 无状态组件：唯一阶段：build
    - 有状态组件
      |  **生命周期阶段**  |                **函数名**             |                    **调用时机与核心任务**                      |
      | ------------------ | --------------------------------------| -------------------------------------------------------------- |
      |       创建阶段     |              createState()            |                 Widget初始化调用，创建State对象                |
      |       创建阶段     |                initState()            |        State对象插入Widget树立刻执行，**仅执行一次**           |
      |       创建阶段     |      didChangeDependencies()          | initState后立即执行一次，当依赖的**inheriteWidget**更新时调用  |
      |   构建与更新阶段   |                  build()              |          **构建UI**方法，**初始化或者更新后多次调用**          |
      |   构建与更新阶段   |           didUpdateWidget()           |            **父组件传入新配置时**调用，用于比较新旧配置        |
      |        销毁阶段    |                deactiveate()          |             当**state对象**从树中暂时**移除时调用**            |
      |        销毁阶段    |                   despose()           |      当State对象被永久移除时调用，释放资源，**仅执行一次**     |

    inheriteWidget：专门用于在Widget树中自顶向下高效地共享数据，顶层组件提供数据，子孙节点直接获取
# 四：事件：点击事件，常见的事件包括滚动点击等。。
# 五：状态更新：setState
# 六：组件
  ### 1.基础容器Container
    ```js
      {
        body:Container(
          width:100,
          height:100,
          // margin: EdgeInsets.all(20),
          decoration:BoxDecoration(color:Colors.blue,borderRadius: BorderRadius.circular(15)),
          child:Text('Hello Container',style:TextStyle(color: Colors.white,fontSize: 20))
        )
      }
    ```
  ### 2.Center居中组件:它的子组件会水平垂直居中，Center没有宽高
    ```js
      {
        body:Center(
          child:Container(
            width:100.0,
            height: 100,
            decoration: BoxDecoration(color: Colors.blue),
            child: Center(
              child:Text('居中内筒')
            ),
          )
        )
      }
    ```
  ### 3.Align对齐组件，控制它的子组件在父容器内的对齐位置
  - alignment对齐方式：
  - Align和Center的区别，Center是Align的一个特例,继承自Align，相当于一个将alignment属性为居中的Align.center
  - 使用场景：当需要将一个组件放置在父容器的特定角落，Align是理想选择
  - 动态尺寸：通过widthFactor和heightFactor，可以创建出与子组件大小成比例的容器
  ### 4.Padding内边距组件
  Container也有padding属性，单一需求用Padding组件，复杂样式用Container
    ```js
      {
        child: Center(
          child:Padding(padding: EdgeInsets.symmetric(vertical: 20,horizontal: 40),child:Container(decoration: BoxDecoration(color:Colors.blue),))
        )
      }
    ```
  ### 5.Column组件
  ### 6.Row组件
  ### 7.Flex弹性布局，flex的子组件通常使用Expanded,Flexible来分配空间
  - direction:主轴方向，决定子组件的排列方向
  - mainAxisAlignment:子组件在主轴方向上的对齐方式
  - crossAxisAlignment:子组件在交叉轴方向上的对齐方式
  - mainAxisSize:Flex容器自身在主轴上的尺寸策略
    ```js
      {
        body:Container(
          child:Flex(
            direction: Axis.vertical,
            children:[
              Container(color: Colors.blue,height: 100,),
              Expanded(
                child: Container(
                  color: Colors.blueGrey,
              )),
              Container(color: Colors.green,height: 100,)
              //  Expanded(
              //   flex:2,
              //   child: Container(
              //     color: Colors.green,
              //     height:100,
              //     width:100
              // ))
            ]
          )
        )
      }
    ```
  ### 8.Wrap流式布局
  - direction:Axis.horizontal(水平)/Axis.vertial
  ### 9.层叠布局：Stack、positioned
    ```js
      {
        body:Stack(
          children: [
            Container(width:100,height: 100 ,color: Colors.grey),
            Positioned(left: 10,bottom:10,child:Container(width:50,height: 50 ,color: Colors.blue))
          ]
        )
      }
    ```
  ### 10.文本组件Text
    - style:
  ### 11.Image图片组件
  ### 12.文本输入组件:TextField


