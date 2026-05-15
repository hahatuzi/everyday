# Dio插件
  ```js
    flutter pub add dio
    Dio().get(url).then().catchError()
  ```

  ### dio封装
    ```js
      void main (List<String> args) {
        Dio().get().then((res) {
          print(res);
        });
      }

      class DioUtils {
        final Dio _dio = Dio();
        DioUtils(){
          _dio.options.baseUrl = "https://geek.itheima.net/v1_0/";
          _dio.options.connectTimeout = Duration(second:10); // 连接超时
          _dio.options.sendTimeout = Duration(second:10); // 发送超时
          _dio.options.receiveTimeout = Duration(second:10); // 接收超时
          _addInterceptor();
          void _addInterceptor () {
            _dio.interceptors.add(InterceptorsWrapper(
              onRequest:(context,handler){
                handler.next(context);
                handler.reject(context);
              },
              onResponse: (context,handler) {
                if (context.statusCode! >= 200 && context.statusCode! < 300){
                  handler.next(context);
                  return;
                }
                handler.reject(DioExpection(requestOptions:context.requestOptions));
              },
              onError:(context,handler){}
            ));
          }
          get(String url, {Map<String, dynamic>? params}){
            return _dio.get(url, queryParameters: params)
          }
        }
      }
    ```
  ### 2.Dio使用案例
    ```js
      @override initState(){
        super.initState()
        _getChannel()
      }
      void _getChannel () {
        DioUtils util = DioUtils()
        Response<dynamic> result= await util.get('channels')
        List data = res["data"]["channels"] as List
        Map<String, dynamic> = data
      }
    ```
