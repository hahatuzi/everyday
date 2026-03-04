# 创建项目
  - (1)第一步：创建项目
  ```js
    // 第一步
    npm create vite@latest react_HDXC --template react-ts
  ```
  - (1)第二步：vite项目配置
  ```js
    npm i less -D
    {
      css: {
        preprocessorOptions: {
          less: {
            javascriptEnabled: true,
          }
        }
      }
    }
  ```