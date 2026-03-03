# 一：eslint
  eslint插件与prettier等多个插件同时使用的时候会导致格式化冲突等问题
  ### 1.作用：
   - (1)静态代码分析，检查代码格式错误或者不推荐的代码习惯
   - (2)提供丰富的自定义规则
   - (3)可以集成prettier等插件，避免多个插件同时使用时导致的错误检测
  ### 2.eslint中使用prettier


# 二：prettier
  项目代码格式化，可以**通过使用prettier插件**或者**在eslint中集成prettier的方式**实现
  ### 1.方式一：通过使用prettier插件实现格式化,本地运行时!!!无关eslint和CICD流程
    ```js
      // 第一步：安装相关插件
      npm i prettier  -D
      // 第二步：新增.prettierrc.json配置文件
      {
        "printWidth": 80,
        "semi": true
      }
      // 第三步：让prettier插件生效：
      // 生效方式一：新建.vscode文件夹-->settings.json
      {
        "editor.defaultFormatter": "esbenp.prettier-vscode",// 明确指定prettier为默认的格式化器
        "editor.formatOnSave": true, // 保存时自动格式化
      }
      // 生效方式二：修改vscode的首选项--设置--搜索format--修改formatter on save为true,default formatter为prettier
    ```
  ### 2.方式二：通过在eslint中使用插件prettier实现格式化
   - **eslint-config-prettier**:关闭 ESLint 中所有与 Prettier 格式化规则‌冲突的规则‌（如缩进、引号、分号等）。
   - **eslint-plugin-prettier**:将 Prettier 的格式化检查‌作为 ESLint 规则‌运行，使不符合 Prettier 规范的代码被标记为 ESLint 错误。让 Prettier 的格式化要求参与 ESLint 的校验流程，并可通过 eslint --fix 自动修复。‌使用方式‌：在 .eslintrc.js 的 plugins 中添加 "prettier"，并设置规则 "prettier/prettier": "error"。
    ```js
      // 第一步：安装相关插件
      npm i eslint-plugin-prettier  -D
      // 第二步：在eslint.config.js中配置prettier
      import js from "@eslint/js";
      import globals from "globals";
      import tseslint from "typescript-eslint";
      import { defineConfig } from "eslint/config";
      import prettier from 'eslint-plugin-prettier'

      export default defineConfig([
        {
          files: ["**/*.{js,mjs,cjs,ts,mts,cts}"],
          languageOptions: { globals: globals.browser },
          plugins: { js, prettier }, // 启用eslint-plugin-prettier插件
          extends: ["js/recommended"],
          rules:{
            "prettier/prettier":[
              "error", // 把 Prettier 格式问题标记为 ESLint 错误
              {
                "printWidth": 100,
                "semi": true,
              } // 这里的配置会覆盖.prettierrc.json的配置
            ]
          }
        },
        tseslint.configs.recommended,
      ]);
    ```

  ### 3.两种方式比较
    - 若项目未使用启用格式化规则的共享配置（如 airbnb），则可能‌不需要‌ eslint-config-prettier。‌
    - 若通过编辑器自动保存时调用 Prettier 格式化，或在 CI 中单独运行 Prettier，则‌可省略‌ eslint-plugin-prettier，以提升 ESLint 性能。‌
    - 新项目可先单独使用 Prettier 进行格式化，ESLint 专注逻辑检查；若需统一校验流程，再引入 plugin:prettier/recommended

  ### 4.为什么需要eslint-plugin-prettier配合使用eslint-config-prettier？
    单独使用eslint-plugin-prettier可能会导致ESLint和Prettier规则冲突。例如，ESLint的indent规则和Prettier的缩进规则可能不一致，导致格式化结果不符合预期。这时候就需要eslint-config-prettier来关闭ESLint中与Prettier冲突的规则。
    ```js
      {
        "extends": "plugin:prettier/recommended"
        // 这个配置会自动启用eslint-plugin-prettier,将prettier/prettier规则设置为"error"
      }
      
    ```
