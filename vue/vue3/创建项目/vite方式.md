# vite方式创建流程
[!参考文章]https://blog.csdn.net/blue_121/article/details/130870776
```js
npm create vite

```
# 二：项目eslint插件添加
```js
npm i eslint  -D
// 生成配置文件
npx eslint --init
```
# 三：项目添加stylelint
[!参考文章]https://blog.csdn.net/blue_121/article/details/130888804?spm=1001.2014.3001.5502
# 四：项目添加husky
利用husky在代码提交之前触发git hook(git在客户端的钩子)，然后执行pnpm run format来自动的格式化我们的代码
```js
// (1)
npm install -D husky
// (2)
npx husky-init
// (3)在.husky/pre-commit文件添加如下命令：

#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npm run format
```
# 五：src文件夹别名配置
```js
// vite.config.js配置
import path from 'path'
export default defineConfig({
  resolve:{
    alias:{
      "@":path.resolve("./src")
    }
  }
})
// tsconfig.json配置
  "compilerOptions": {
    "baseUrl": "./", // 解析非相对模块的基地址，默认为当前目录
    "paths": {
      "@/*":["src/*"] // 路径映射
    }
  }
```
# 六：环境变量