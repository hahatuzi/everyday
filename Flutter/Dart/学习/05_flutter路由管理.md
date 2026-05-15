# 基本路由：适合页面不多，跳转逻辑简单的场景
  - 无需提前注册路由，跳转时创建**MaterialPageRoute实例**即可
  - Navigator.push(BuildContext context, Route route)
  - Navigator.pop(BuildContext context)
    ```js
      import 'dart:math';

      import 'package:flutter/material.dart';

      void main() {
        runApp(MainPage());
      }

      class MainPage extends StatelessWidget {
        @override
        Widget build(BuildContext context) {
          return MaterialApp(
          title:"Hello Flutter",
          theme: ThemeData(scaffoldBackgroundColor: Colors.amber),
          home: ListPage()
        );}
      }

      class ListPage extends StatefulWidget {
        ListPage({Key? key}) : super(key: key);

        @override
        _ListPageState createState() => _ListPageState();
      }

      class _ListPageState extends State<ListPage> {
        @override
        Widget build(BuildContext context) {
          return Scaffold(
            appBar: AppBar(
              title:Text('列表页'),
            ),
            body: ListView.builder(
              itemCount: 100,
              itemBuilder: (BuildContext context, int index){
                return GestureDetector(
                  onTap:(){
                    Navigator.push(context, MaterialPageRoute(builder: (context) => DetailPage(id:index + 1)));
                  },
                  child:Container(
                    color: Colors.blue,
                    margin:EdgeInsets.only(top:10),
                    height: 100,
                    alignment: Alignment.center,
                    child:Text('列表页${index + 1}',style:TextStyle(color:Colors.white,fontSize: 16))
                  )
                );
              }
            ),
          );
        }
      }

      class DetailPage extends StatefulWidget {
        final int? id;
        DetailPage({Key? key, this.id}) : super(key: key);

        @override
        _DetailPageState createState() => _DetailPageState();
      }

      class _DetailPageState extends State<DetailPage> {
        @override
        void initState(){
          super.initState();
          print(widget.id);
        }
        @override
        Widget build(BuildContext context) {
          return Scaffold(
            appBar: AppBar(title:Text('详情页')),
            body:Center(
              child:TextButton(onPressed: (){Navigator.pop(context);},child:Text("返回上级页面${widget.id}"))
            )
          );
        }
      }
    ```

# 命名路由
  - 应用页面增多后，使用命名路由提高代码可维护性
  - 需要先在MaterialApp中注册一个**路由表routes**，并设置**initialRoute**
  - pushNamed:进入新页面
  ```js
    void main() {
      runApp(MaterialApp(
        initialRoute: '/list',
        routes:{
          '/list':(context)=> ListPage(),
          '/detial':(context)=> DetailPage()
        })
      );
    }

    onTap:(){
              Navigator.pushNamed(context, '/detail');
              // Navigator.push(context, MaterialPageRoute(builder: (context) => DetailPage()));
            },
  ```

# 路由传递参数
  ### 1.基础路由传参
  ### 1.命名路由传参
  - 传递参数(命名路由)：**Navigator.pushNamed(context,地址，arguments:{参数})**
  - 传递参数(命名路由)**ModalRout.of(context)?.settings.arguments**
  - 接收实际：**initState获取不到路由参数**，放置在**Future.microtask(异步微任务)中**
    ```js
      import 'dart:math';

      import 'package:flutter/material.dart';

      void main() {
        runApp(MainPage());
      }

      class MainPage extends StatelessWidget {
        @override
        Widget build(BuildContext context) {
          return MaterialApp(
            initialRoute: '/list',
            routes:{
              '/list':(context)=> ListPage(),
              '/detail':(context)=> DetailPage()
            }
          // title:"Hello Flutter",
          // theme: ThemeData(scaffoldBackgroundColor: Colors.amber),
          // home: ListPage()
        );}
      }

      class ListPage extends StatefulWidget {
        ListPage({Key? key}) : super(key: key);

        @override
        _ListPageState createState() => _ListPageState();
      }

      class _ListPageState extends State<ListPage> {
        @override
        Widget build(BuildContext context) {
          return Scaffold(
            appBar: AppBar(
              title:Text('列表页'),
            ),
            body: ListView.builder(
              itemCount: 100,
              itemBuilder: (BuildContext context, int index){
                return GestureDetector(
                  onTap:(){
                    Navigator.pushNamed(context, '/detail',arguments: {'id':index + 1});
                    // Navigator.push(context, MaterialPageRoute(builder: (context) => DetailPage()));
                  },
                  child:Container(
                    color: Colors.blue,
                    margin:EdgeInsets.only(top:10),
                    height: 100,
                    alignment: Alignment.center,
                    child:Text('列表页${index + 1}',style:TextStyle(color:Colors.white,fontSize: 16))
                  )
                );
              }
            ),
          );
        }
      }

      class DetailPage extends StatefulWidget {
        DetailPage({Key? key}) : super(key: key);

        @override
        _DetailPageState createState() => _DetailPageState();
      }

      class _DetailPageState extends State<DetailPage> {
        String _id = '';
        void initState(){
          super.initState();
          Future.microtask((){

          if(ModalRoute.of(context) != null){
            print('获取到了路由参数');
            Map<String,dynamic> params = ModalRoute.of(context)!.settings.arguments as Map<String,dynamic>;
            print(params['id']);
            _id = params['id'].toString();
            setState(() {
              
            });
          } else {
            print('获取不到路由参数');
          }
          });
        }
        @override
        Widget build(BuildContext context) {
          return Scaffold(
            appBar: AppBar(title:Text('详情页')),
            body:Center(
              child:Column(
                children: [
                  TextButton(
                    onPressed: (){
                      Navigator.pushNamed(context, '/list');
                    },
                    child:Text("返回列表页${_id}")),
                  TextButton(
                    onPressed: (){
                      Navigator.pop(context);
                    },
                    child:Text("返回上级页面")),
                ],
              )
            )
          );
        }
      }

    ```
# 动态路由与高级控制：onGenerateRoute和onUnknownRoute根据参数动态生成页面，或者实现路由拦截
  - onGenerateRoute动态创建不同的Route
  - onUnknownRoute:跳转一个未在路由表中注册，也未在onGenerateRoute中处理的路由，会调用此回调，通常显示404页面
