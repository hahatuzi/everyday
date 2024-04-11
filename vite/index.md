# 1.webpack的缺点
# 2.es module的规范
# 3.vite是什么
# 4.vite的基本安装和使用
 ### (1)为什么要使用npm create vite来创建项目，npm create又是什么？
 [!参考链接]https://blog.csdn.net/Cyj1414589221/article/details/128191826
 ```js
  npm init// npm create // npm init中的init有两个别名create和innit，所以npm init和npm create是等价的
  npm exec <command>  // 用来执行本地报或者远程包中的命令，可以简写为 npx <command>
  npm init // 是用来创建一个package.json文件
  npm init initializer 
  // initializer 本质是一个名字叫做create-initializer的包，在这个包中会有一个create-initializer的命令
  // 执行npm init initilizer --->  会先去安装create-initilizer这个包  ---> 然后过npm exec  create-initializer执行包
 ```
# 5.vite的编译结果
# 6.vite编译结果分析
# 7.vite的配置文件
  ```js
  // vite.config.js解读
  export default defineConfig({
    css:{
      modules:{
        localsConvention:'camemlCaseOnly', // 修改生成的配置对象的key的展示形式
        scopeBehavior:'local', // 配置当前的模块化行为是模块化还是全局化
        hashPrefix:'', // hash拼接字符串
        globalModulePaths:[] //　不希望参与到ｃｓｓ模块化的路径
      },
      preprocessOptions:{
        less:{
          math:'always',
          globalVars:{
            // 全局变量
          }
        }
      }
    }
  })
  ```

# 8.vite处理css等静态资源文件
```js
  {
    build:{
      rollupOptions:{
        output:{ // 控制打包输出的文件名格式
          assetsFileNames:'[hash].[name].[ext]' // 
        }
      },
      assetsInlineLimit:409600, // 4000kb
      outDir:'dist',
      assetsDir:'static'
    }
  }
```
# 9.vite的插件使用
# 10.vite与ts结合使用
# 11.vite的构建原理

# 12：vite的基于esbuild的依赖预构建
[!参考链接]https://zhuanlan.zhihu.com/p/467325485
目的：

(1)支持commonJS
(2)解决原生js的模块化规范不同的问题，Vite 会先将以 CommonJS 或 UMD 形式提供的依赖项转换为 ES 模块。
(3)减少模块和请求数量，为了提高页面渲染性能问题，如果一个模块内引入了很多个其他依赖模块，那么该模块会将这些依赖模块转换成单个依赖项,并缓存在node_modules/.vite/deps中

```js
  // 比如lodash-es的内部模块导入关系是
  export {default as a} from './a.js'
  export {default as b} from './b.js'
  export {default as c} from './c.js'
  ...
  // 当import {isArray} from 'lodash-es'的时候，lodash会请求加载所有类似上述的a,bc,文件依赖模块，
  // 所以vite将这些资源的导入方式重写到了一个模块中，以减少请求模块数量！！！
  optimizeDeps:{
    exclude:['lodash-es']// lodash-es文件不进行依赖预构建,这样vite就不会将lodash-es重写到一个模块中，会变成旧的几百个模块请求
  }
```

# 13：vite的环境变量和模式
- vite的loadEnv：执行过程:直接找到.env文件并解析其中的环境变量，然后解析mode变量传递的值进行拼接成.env.development，解析development中的环境变量

- vite的import.meta.env对象上包含了环境变量，环境变量包括以下信息：
（1）import.meta.env.MODE：应用运行的模式
（2）import.meta.env.BASE_URL:部署应用是的基本URL，由base配置项决定
（3）import.meta.env.PROD: {boolean} 应用是否运行在生产环境（使用 NODE_ENV='production' 运行开发服务器或构建应用时使用 NODE_ENV='production' ）。
（4）import.meta.env.DEV: {boolean} 应用是否运行在开发环境 (永远与 import.meta.env.PROD相反)。
（5）import.meta.env.SSR: {boolean} 应用是否运行在 server 上。

# 14.vite对css的处理
postcss:postcss可以实现对less等语法进行预编译然后通过补足等多种手段，让最终的css适配浏览器等多端

# 15.vite的性能优化
  ### （1）gzip压缩
    [!参考链接]https://developer.aliyun.com/article/1139829

    客户端的开启gzip压缩是为了减少原来的服务器压缩的压力，
    旧的方式是客户端**每次请求服务器**的时候，**服务器**都要对资源**先进行一番压缩**，**然后再返回**给客户端，
    然后大家发现服务器**每次都要压缩有点儿浪费时间**，所以就出现了客户端**打包时先对资源进行压缩**，将压缩后的资源也作为服务器资源，这样服务器每次在每次接收到请求时就可以直接读取压缩资源了！！然后客户端再**对响应头中有gzip格式的文件进行解压**获取文件内容

    ```js
      // 服务端的压缩方式：nginx,使用httpGip模块
      gzip  on;           // 开启或者关闭gzip模块
      gzip_buffers 4 16k; //  设置系统获取几个单位的缓存用于存储gzip的压缩结果数据流
      gzip_comp_level 6;  //  gzip压缩比，1 压缩比最小处理速度最快 
      gzip_types text/plain application/javascript text/css application/xml text/javascript application/x-httpd-php;
      // 匹配MIME类型进行压缩，（无论是否指定）"text/html"类型总是会被压缩的
      
    ```
    ```js
    // 客户端的压缩方式：
    // webpack
    // 这里使用的 vue.config.js, webpack.config.js 里面内容大部分相同，只是vue.config.js里面是链式调用的。
    const compressionWebpackPlugin = require('compression-webpack-plugin')
    {
      configureWebpack: {
        plugins: [new compressionWebpackPlugin({
          filename: '[path].gz[query]', //压缩后的文件名
          algorithm: 'gzip', // 压缩格式 有：gzip、brotliCompress,
          test: /\.(js|css|svg)$/,
          threshold: 10240,// 只处理比这个值大的资源，按字节算
          minRatio: 0.8, //只有压缩率比这个值小的文件才会被处理，压缩率=压缩大小/原始大小，如果压缩后和原始文件大小没有太大区别，就不用压缩
          deleteOriginalAssets: false //是否删除原文件，最好不删除，服务器会自动优先返回同名的.gzip资源，如果找不到还可以拿原始文件
        })],
      }
    }
    // vite
    import viteCompression from 'vite-plugin-compression';
    {
      plugins: [
        viteCompression()
      ],
    }
    // nginx对应配置，配置启动gzip模块， 然后优先使用本地压缩好的文件
      gzip_static on; // 启动模块。您应该确保压缩和解压文件的时间戳匹配
      gzip_http_version   1.1; // 版本，默认是1.1， 使用 gzip_static,就是要 1.1的版本
      gzip_proxied        expired no-cache no-store private auth; //Nginx作为反向代理的时候启用，开启或者关闭后端服务器返回的结果
    ```

  ### （2）动态导入
  ```js
  function import (path) {
    return new Promise((resolve) => {
      webpack_require.e().then(() => {
        const result = await webpack_require(path)
      })
    })
  }
  // import先创建script标签指向对应的js文件，当路由进入对应的path时，才会进行require按需导入对应的script标签到body中
  ```