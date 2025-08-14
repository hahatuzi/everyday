### 脚手架
帮助我们把webpack等相关配置都处理好，个人理解的脚手架除了合并打包编译常规流程外还要包含eslint，环境配置，常用插件等基础的搭建
### vue/cli练习结果，能够自己实现一套适合公司的脚手架
### 学习安排
#### 1.webpack
### 2.eslint
### 3.babel
### 4.TypeScript
### 5.Router
### 6.vuex
### 7.cssLoader
### 8.formatter
### 9.axios
# 个人小结
如果想搭建一个通用的vue项目基础模板，需要经过哪些步骤和配置
## 第一步：技术选型
技术的选型一般简单选个框架和开发语言即可
## 第二步：安装项目依赖
为项目安装开发必备的一些依赖：
#### (1)axios
包括防止重复请求处理，二次封装请求处理
将请求数据线暂时存放在cookie中一秒钟，如果在这一秒钟内重复请求
#### (2)router,//其中vue2使用的是3.X版本的路由，vue3使用的是4.X版本
  注意点：
  1.路由存放位置，前端或者后端？
  2.路由懒加载方式：按需导入
  ```js
    router.addRoute(accessRoutes) // 动态添加可访问路由表
    next({ ...to, replace: true }) // hack方法 确保addRoutes已完成
  ```
#### (3)eslint,
#### (4)vuex,
#### (5)element-ui/antd,
#### (6)less-loader,
#### (7)loashde,
## 第三步：对依赖和打包相关的内容做配置
环境配置，打包配置，路由配置，存储配置，请求配置，页面搭建配置

## vue中的设计模式
- 单例模式store
- 工厂模式createElement
- 发布订阅模式
- 观察者模式;watcher和dep
- 代理模式；_data
- 策略模式；针对不同的行为提供不同的策略