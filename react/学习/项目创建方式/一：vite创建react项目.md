# 通过 vite 创建 react 项目,完整过程！！！

(1)第一步：npm init vite
(2)第二步：配置项目基本插件,使用@vitejs/plugin-react -D 安装 vite 针对 react 全局注入的插件

```js
"scripts": {
    "dev": "vite --host --port 3002",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^8.1.3",
    "react-router-dom": "^6.18.0",
    "redux": "^4.2.1",
    "reset-css": "^5.0.2" // import 'reset-css' 在main.js的头部引入
  },
```

(3)第三步：修改 vite.config.js 将@指向 src 文件夹

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path"; // 如果使用的是ts的话，要先安装node库的ts声明配置：npm i -D @types/node
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

(4)第四步：全局 css 样式管理,组件化 module.scss 的样式管理,全局样式变量管理

```js
// =================标准样式添加normalize.css
// npm i normalize.css
// ==================一：全局css样式管理==================
// (1)npm i sass --save-dev
// (2)创建并在main.tsx中引用src/styles/global.scss文件
// ==================scss文件参考===============
// $color:#eee;
// body{
//   background-color: $color;
//   user-select: none;
// }
// ==================二：组件的scss开发===============
// 新增组件的module.scss来管理组建的样式，防止样式冲突
// ==================全局样式变量管理=============
// (1)修改vite.config.ts配置文件

// ====================三：vite.config.ts文件参考=======================
export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "./src/styles/sassConfig.scss";`,
        // 全局倒入less变量
        additionalData:`@import './src/styles/var.less'`
      },
    },
  },
});
// (2)创建sassConfig.scss文件，并书写变量
// =================sassConfig.scss全局变量文件参考===============
// $color: orange;
```

(5)修改 tsconfig.json，当输入@时提示 src 下的文件路径

```js
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "@/*":["src/*"]
    },
  },
```

# [!React 从 CRA 到 Vite 迁移笔记]https://www.jianshu.com/p/b5c4436b744c
