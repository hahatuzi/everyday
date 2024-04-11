# 1.构建流程对比：
  - webpack
    entry -->  route1  --> module  --> bundle -->   server ready
          -->  route2  --> module
          -->  route3  --> module (等所有的模块都构建完成后才bundle)
  - vite
    server ready -->  route1  --> module (按需构建路由对应的模块)
                 -->  route2  --> module
                 -->  route3  --> module