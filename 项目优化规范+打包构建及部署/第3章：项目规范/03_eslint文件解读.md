# 1.eslint解读
[!参考文章]https://blog.51cto.com/u_11887782/5724620
  ```js
    module.exports = {
      root: true,
      env: {
        browser: true,
        es2021: true,
        node: true,
      },
      // 解析器类型：从eslint的解析器中选择合适的解析器：esprima默认解析器，babel-eslint：balel解析器，
      parser: "vue-eslint-parser",
      extends: [
        // https://eslint.vuejs.org/user-guide/#usage
        "./.eslintrc-auto-import.json",
        "prettier",
        "plugin:vue/vue3-recommended", // 除了包含vue3-essential的所有规则外还添加了别的规则
        "plugin:vue/vue3-essential", // vue3语法规则
        "plugin:@typescript-eslint/recommended", // ts语法规则校验
        "plugin:prettier/recommended",
      ],
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        parser: "@typescript-eslint/parser",
        project: "./tsconfig.*?.json",
        createDefaultProgram: false,
        extraFileExtensions: [".vue"],
      },
      // eslint第三方插件
      plugins: ["vue", "@typescript-eslint"],
      // eslint规则
      rules: {
        // https://eslint.vuejs.org/rules/#priority-a-essential-error-prevention
        "vue/multi-word-component-names": "off",
        "vue/no-v-model-argument": "off",
        "vue/script-setup-uses-vars": "error",
        "vue/no-reserved-component-names": "off",
        "vue/custom-event-name-casing": "off",
        "vue/attributes-order": "off",
        "vue/one-component-per-file": "off",
        "vue/html-closing-bracket-newline": "off",
        "vue/max-attributes-per-line": "off",
        "vue/multiline-html-element-content-newline": "off",
        "vue/singleline-html-element-content-newline": "off",
        "vue/attribute-hyphenation": "off",
        "vue/require-default-prop": "off",
        "vue/require-explicit-emits": "off",
        "vue/html-self-closing": [
          "error",
          {
            html: {
              void: "always",
              normal: "never",
              component: "always",
            },
            svg: "always",
            math: "always",
          },
        ],

        "@typescript-eslint/no-empty-function": "off", // 关闭空方法检查
        "@typescript-eslint/no-explicit-any": "off", // 关闭any类型的警告
        "@typescript-eslint/no-non-null-assertion": "off",
        "@typescript-eslint/ban-ts-ignore": "off",
        "@typescript-eslint/ban-ts-comment": "off",
        "@typescript-eslint/ban-types": "off",
        "@typescript-eslint/explicit-function-return-type": "off",
        "@typescript-eslint/no-explicit-any": "off", // 禁止使用any类型
        "@typescript-eslint/no-var-requires": "off",
        "@typescript-eslint/no-empty-function": "off",
        "@typescript-eslint/no-use-before-define": "off",
        "@typescript-eslint/no-non-null-assertion": "off",
        "@typescript-eslint/explicit-module-boundary-types": "off",
        "@typescript-eslint/no-unused-vars": "off",

        "prettier/prettier": [
          "error",
          {
            endOfLine: "auto",
            useTabs: false, // 不使用制表符
          },
        ],
      },
      // 为特定的文件指定处理器
      // eslint不能对html文件生效
      overrides: [
        {
          files: ["*.html"],
          processor: "vue/.vue",
        },
      ],
      // https://eslint.org/docs/latest/use/configure/language-options#specifying-globals
      globals: {
        OptionType: "readonly",
      },
    };

  ```


# 2.eslint完整使用案例
    ```js
    // https://eslint.org/docs/latest/use/configure/configuration-files-new

      import eslint from "@eslint/js";
      import pluginVue from "eslint-plugin-vue";
      import vueParser from "vue-eslint-parser";
      import pluginTypeScript from "@typescript-eslint/eslint-plugin";
      import parserTypeScript from "@typescript-eslint/parser";
      import globals from "globals";
      import configPrettier from "eslint-config-prettier";

      // 解析自动导入配置
      import fs from "node:fs";
      let autoImportGlobals = {};
      try {
        autoImportGlobals = JSON.parse(fs.readFileSync("./.eslintrc-auto-import.json", "utf-8")).globals || {};
      } catch (error) {
        // 文件不存在或解析错误时使用空对象
        console.warn("Could not load auto-import globals", error);
      }

      // Element Plus组件
      const elementPlusComponents = {
        // Element Plus 组件添加为全局变量，避免 no-undef 报错
        ElInput: "readonly",
        ElSelect: "readonly",
        ElSwitch: "readonly",
        ElMessage: "readonly",
        ElMessageBox: "readonly",
        ElNotification: "readonly",
        ElTree: "readonly",
      };

      export default [
        // 全局配置
        {
          // 指定要检查的文件
          files: ["**/*.js", "**/*.ts", "**/*.vue"],
          ignores: ["node_modules/**", "dist/**", "build/**"],
          languageOptions: {
            ecmaVersion: 2022,
            sourceType: "module",
            globals: {
              ...globals.browser, // 浏览器环境全局变量
              ...globals.node, // Node.js 环境全局变量
              ...autoImportGlobals, // 自动导入的 API 函数
              ...elementPlusComponents, // Element Plus 组件
              // 全局类型定义，解决 TypeScript 中定义但 ESLint 不识别的问题
              PageQuery: "readonly",
              PageResult: "readonly",
              OptionType: "readonly",
              ResponseData: "readonly",
              ExcelResult: "readonly",
              TagView: "readonly",
              AppSettings: "readonly",
              __APP_INFO__: "readonly",
            },
            parser: parserTypeScript,
            parserOptions: {
              sourceType: "module",
            },
          },
          rules: {
            // 全局规则
            "no-unused-vars": [
              "error",
              {
                vars: "all",
                args: "after-used",
                ignoreRestSiblings: true,
                argsIgnorePattern: "^_", // 忽略以下划线开头的参数
                varsIgnorePattern: "^[A-Z][A-Z0-9_]*$", // 忽略全大写的常量/枚举
              },
            ],
            // 禁用未定义变量检查，TypeScript 已处理类型检查
            "no-undef": "off",
          },
        },

        // 基础 JavaScript 配置
        eslint.configs.recommended,

        // Vue 配置
        {
          files: ["**/*.vue"],
          plugins: {
            vue: pluginVue,
          },
          languageOptions: {
            parser: vueParser,
            parserOptions: {
              ecmaVersion: 2022,
              sourceType: "module",
              parser: parserTypeScript,
            },
          },
          processor: pluginVue.processors[".vue"],
          rules: {
            "vue/multi-word-component-names": "off",
            "vue/no-v-html": "off",
            "vue/require-default-prop": "off",
            "vue/html-self-closing": [
              "error",
              {
                html: {
                  void: "always",
                  normal: "never",
                  component: "always",
                },
              },
            ],
            "vue/no-unused-vars": "off",
          },
        },

        // TypeScript 配置
        {
          files: ["**/*.ts", "**/*.tsx", "**/*.vue"],
          plugins: {
            "@typescript-eslint": pluginTypeScript,
          },
          rules: {
            "@typescript-eslint/no-explicit-any": "off",
            "@typescript-eslint/no-empty-function": "off",
            "@typescript-eslint/no-empty-object-type": "off",
            "@typescript-eslint/ban-ts-comment": "off",
            "@typescript-eslint/no-non-null-assertion": "off",
            "@typescript-eslint/no-unused-vars": [
              "error",
              {
                vars: "all",
                args: "after-used",
                ignoreRestSiblings: true,
                argsIgnorePattern: "^_", // 忽略以下划线开头的参数
                varsIgnorePattern: "^[A-Z][A-Z0-9_]*$", // 忽略全大写的常量/枚举
              },
            ],
          },
        },

        // CURD 组件配置
        {
          files: ["**/components/CURD/**/*.{ts,vue}"],
          rules: {
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": "off",
          },
        },

        // Prettier 集成
        {
          rules: {
            ...configPrettier.rules,
          },
        },
      ];

    ```

# 3.eslint自定义rules规则
  - 第一步：**rule定义**：针对需求编写一个rule,原理是通过ast，通过ast节点处理
      ```js
        // 规则的本质是一个对象，
        // 插件化体系中，这个对象的属性约束就是我们讲的插件化协议
        export const noChineseVars = {
          // 插件的元信息
          meta:{
            messages:{
              noChineseName:'不允许使用中文' // noChineseName对应Identifier中的messageId
            }
          },
          // 插件的入口,插件上下文
          create (context) {
            return {
              // 访问者模式，访问到某一个ast节点时就进行处理
              VariableDeclaration(node){
                console.log('VariableDeclaration',node);
              },
              VariableDeclarator(node){
                console.log(node);
              },
              Identifier(node){
                console.log(node);
                if (node.name == 'chinese') {
                  // 上报错误
                  context.report({
                    node,
                    messageId:'noChineseName'
                  })
                }
              },
              Literal(node){
                console.log(node);
              },
            }
          }
        }
      ```
    - 第二步：**定义plugins插件，将rule进行插件化**，提供给外部使用
      ```js
        // 规则的本质是一个对象，
        // 插件化体系中，这个对象的属性约束就是我们讲的插件化协议
        export const noChineseVars = {
          // 插件的元信息
          meta:{
            messages:{
              noChineseName:'不允许使用中文' // noChineseName对应Identifier中的messageId
            }
          },
          // 插件的入口,插件上下文
          create (context) {
            return {
              // 访问者模式，访问到某一个ast节点时就进行处理
              VariableDeclaration(node){
                console.log('VariableDeclaration',node);
              },
              VariableDeclarator(node){
                console.log(node);
              },
              Identifier(node){
                console.log(node);
                if (node.name == 'chinese') {
                  context.report({
                    node,
                    messageId:'noChineseName'
                  })
                }
              },
              Literal(node){
                console.log(node);
              },
            }
          }
        }

      ```
    - 第三步：将插件引入到eslint配置文件中进行使用
      ```js
        import {eslintChinesePlugin} from './eslint/plugins/eslint-plugin-chinese.js'
        export default{
          files:['**/*.ts','**/*.vue'],
          ignores:['eslint.config.js'],
          plugins:{
            'chinese':eslintChinesePlugin // 插件注册，插件的名称就是规则的作用域rules:{'chinese/no-chinese-vars':"error"}
          },
          rules:{
            "chinese/no-chinese-vars":"error"
          }
        }
      ```
 

# eslint相关问题
  ### eslint和prettier概念
    - prettier代码格式化，
  - 是否了解eslint9,或者oxclint
  - voidzero为什么需要通过rust重构整个工具链：统一ast,建构，叫妖孽，格式化等所有环境共用一个ast

# eslint9

[!参考学习视频--妙码学院eslint]https://www.bilibili.com/video/BV1USEjzZE6a?spm_id_from=333.788.player.switch&vd_source=afbd897dda8c1c6166fce57f249edafd&p=14