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
# 七：vite常用插件
```js
// 第一步：新建vite/plugins/index.js文件
import vue from '@vitejs/plugin-vue'
import commonjs from '@rollup/plugin-commonjs'

import createAutoImport from './auto-import'
import createSvgIcon from './svg-icon'
import createCompression from './compression'
import createSetupExtend from './setup-extend'

export default function createVitePlugins(viteEnv, isBuild = false) {
    const vitePlugins = [commonjs(), vue()]
    vitePlugins.push(createAutoImport())
	vitePlugins.push(createSetupExtend())
    vitePlugins.push(createSvgIcon(isBuild))
	isBuild && vitePlugins.push(...createCompression(viteEnv))
    return vitePlugins
}
// 第二步：新建auto-import等文件...引入插件
import setupExtend from 'unplugin-vue-setup-extend-plus/vite'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import autoImport from 'unplugin-auto-import/vite'

// 第三步：在vite.config.js中引入插件
import createVitePlugins from './vite/plugins'

export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd())
  const { VITE_APP_BASE_PATH, VITE_APP_BASE_API, VITE_APP_BASE_URL } = env
  return {
    // 默认情况下，vite 会假设你的应用是被部署在一个域名的根路径上
    // 例如 https://www.ruoyi.vip/。如果应用被部署在一个子路径上，你就需要用这个选项指定这个子路径。例如，如果你的应用被部署在 https://www.ruoyi.vip/admin/，则设置 baseUrl 为 /admin/。
    base: VITE_APP_BASE_PATH,
    plugins: createVitePlugins(env, command === 'build')
  }
})
```