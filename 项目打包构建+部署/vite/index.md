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
  import {fileURLToPath,URL} from 'path'
  export default defineConfig({
    resolve:{
      alias:{
        '@':fileURLToPath(new URL('./src', import.meta.url))
      }
    }
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
      },
			postcss: {
				plugins: [
					postCssPxToRem({
						rootValue: 37.5, // 自适应，px>rem转换
						propList: ["*"], // 需要转换的属性，这里选择全部都进行转换
						selectorBlackList: ["norem"], // 过滤掉norem-开头的class，不进行rem转换
					}),
				],
			},
    }
  })
  ```

# 8.vite处理css等静态资源文件
```js
  // 构建配置
  build: {
    assetsInlineLimit:409600, // 4000kb
    outDir:'dist',
    assetsDir:'static',
    chunkSizeWarningLimit: 2000, // 消除打包大小超过500kb警告
    minify: "terser", // Vite 2.6.x 以上需要配置 minify: "terser", terserOptions 才能生效
    terserOptions: {
      compress: {
        keep_infinity: true, // 防止 Infinity 被压缩成 1/0，这可能会导致 Chrome 上的性能问题
        drop_console: true, // 生产环境去除 console
        drop_debugger: true, // 生产环境去除 debugger
      },
      format: {
        comments: false, // 删除注释
      },
    },
    rollupOptions: {
      output: {
        // 用于从入口点创建的块的打包输出格式[name]表示文件名,[hash]表示该文件内容hash值
        entryFileNames: "js/[name].[hash].js",
        // 用于命名代码拆分时创建的共享块的输出命名
        chunkFileNames: "js/[name].[hash].js",
        // 用于输出静态资源的命名，[ext]表示文件扩展名
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split(".");
          let extType = info[info.length - 1];
          // console.log('文件信息', assetInfo.name)
          if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
            extType = "media";
          } else if (/\.(png|jpe?g|gif|svg)(\?.*)?$/.test(assetInfo.name)) {
            extType = "img";
          } else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
            extType = "fonts";
          }
          return `${extType}/[name].[hash].[ext]`;
        },
        manualChunks (id) {
          // id:所有文件的绝对路径，将node_modules中的代码单独打包成一个js文件
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString()
          }
        }
      },
    },
  }
```
# 9.vite的插件使用
  - unplugin-vue-components:vant组件库的按需导入插件
  - vite-plugin-imp
# 10.vite与ts结合使用
# 11.vite的构建原理

# 12：vite的基于esbuild的依赖预构建


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

# vite集成eslint和prettier
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

# 16.导入import.meta.glob
  ```js
    const modules = import.meta.glob('./dir/*.js')
    Object.entries(modules).forEach([k,v] => {
      v().then(m => console.log(k + ':' + m.default))
    })
  ```

