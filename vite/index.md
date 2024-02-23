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
# 8.vite处理css等静态资源文件
# 9.vite的插件使用
# 10.vite与ts结合使用
# 11.vite的构建原理

# 12：vite的依赖预构建
目的：
(1)解决原生js的模块化规范不同的问题，Vite 会先将以 CommonJS 或 UMD 形式提供的依赖项转换为 ES 模块。
(2)为了提高页面渲染性能问题，如果一个模块内引入了很多个其他依赖模块，那么该模块会将这些依赖模块转换成单个依赖项,并缓存在node_modules/.vite/deps中
# 13：vite的环境变量和模式
vite的import.meta.env对象上包含了环境变量，环境变量包括以下信息：
（1）import.meta.env.MODE：应用运行的模式
（2）import.meta.env.BASE_URL:部署应用是的基本URL，由base配置项决定
（3）import.meta.env.PROD: {boolean} 应用是否运行在生产环境（使用 NODE_ENV='production' 运行开发服务器或构建应用时使用 NODE_ENV='production' ）。
（4）import.meta.env.DEV: {boolean} 应用是否运行在开发环境 (永远与 import.meta.env.PROD相反)。
（5）import.meta.env.SSR: {boolean} 应用是否运行在 server 上。
# 14.vite对css的处理
postcss:postcss可以实现对less等语法进行预编译然后通过补足等多种手段，让最终的css适配浏览器等多端