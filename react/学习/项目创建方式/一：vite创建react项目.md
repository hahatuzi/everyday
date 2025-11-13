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

(3)第三步：修改 vite.config.js 将@指向 src 文件夹,修改 tsconfig.json，当输入@时提示 src 下的文件路径

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

	// 如果是typescript需要在tsconfig.json同时配置,修改 tsconfig.json，当输入@时提示 src 下的文件路径
		compilerOptions：{
		// 解析非相对模块名的基准目录
			"baseUrl": "./",
			// 模块名到基于 baseUrl的路径映射的列表。
			"paths": {
				"@": ["src"],
				"@/*": ["src/*"]
			}
		}
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

(5)prettier插件安装 npm i prettier eslint-config-prettier eslint-plugin-prettier -D

```js

```

# [!React 从 CRA 到 Vite 迁移笔记]https://www.jianshu.com/p/b5c4436b744c

# eslint配置
 ```js
 // @see: http://eslint.cn

module.exports = {
	settings: {
		react: {
			version: "detect"
		}
	},
	root: true,
	env: {
		browser: true,
		node: true,
		es6: true
	},
	/* 指定如何解析语法 */
	parser: "@typescript-eslint/parser",
	/* 优先级低于 parse 的语法解析配置 */
	parserOptions: {
		ecmaVersion: 2020,
		sourceType: "module",
		jsxPragma: "React",
		ecmaFeatures: {
			jsx: true
		}
	},
	plugins: ["react", "@typescript-eslint", "react-hooks", "prettier"],
	/* 继承某些已有的规则 */
	extends: [
		"eslint:recommended",
		"plugin:react/recommended",
		"plugin:@typescript-eslint/recommended",
		"plugin:react/jsx-runtime",
		"plugin:react-hooks/recommended",
		"prettier",
		"plugin:prettier/recommended"
	],
	/*
	 * "off" 或 0    ==>  关闭规则
	 * "warn" 或 1   ==>  打开的规则作为警告（不影响代码执行）
	 * "error" 或 2  ==>  规则作为一个错误（代码不能执行，界面报错）
	 */
	rules: {
		// eslint (http://eslint.cn/docs/rules)
		"no-var": "error", // 要求使用 let 或 const 而不是 var
		"no-multiple-empty-lines": ["error", { max: 1 }], // 不允许多个空行
		"no-use-before-define": "off", // 禁止在 函数/类/变量 定义之前使用它们
		"prefer-const": "off", // 此规则旨在标记使用 let 关键字声明但在初始分配后从未重新分配的变量，要求使用 const
		"no-irregular-whitespace": "off", // 禁止不规则的空白

		// typeScript (https://typescript-eslint.io/rules)
		"@typescript-eslint/no-unused-vars": "error", // 禁止定义未使用的变量
		"@typescript-eslint/no-inferrable-types": "off", // 可以轻松推断的显式类型可能会增加不必要的冗长
		"@typescript-eslint/no-namespace": "off", // 禁止使用自定义 TypeScript 模块和命名空间。
		"@typescript-eslint/no-explicit-any": "off", // 禁止使用 any 类型
		"@typescript-eslint/ban-ts-ignore": "off", // 禁止使用 @ts-ignore
		"@typescript-eslint/ban-types": "off", // 禁止使用特定类型
		"@typescript-eslint/explicit-function-return-type": "off", // 不允许对初始化为数字、字符串或布尔值的变量或参数进行显式类型声明
		"@typescript-eslint/no-var-requires": "off", // 不允许在 import 语句中使用 require 语句
		"@typescript-eslint/no-empty-function": "off", // 禁止空函数
		"@typescript-eslint/no-use-before-define": "off", // 禁止在变量定义之前使用它们
		"@typescript-eslint/ban-ts-comment": "off", // 禁止 @ts-<directive> 使用注释或要求在指令后进行描述
		"@typescript-eslint/no-non-null-assertion": "off", // 不允许使用后缀运算符的非空断言(!)
		"@typescript-eslint/explicit-module-boundary-types": "off", // 要求导出函数和类的公共类方法的显式返回和参数类型

		// react (https://github.com/jsx-eslint/eslint-plugin-react)
		"react-hooks/rules-of-hooks": "off",
		"react-hooks/exhaustive-deps": "off"
	}
};

 ```