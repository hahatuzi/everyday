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

# 三：