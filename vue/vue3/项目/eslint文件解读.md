# eslint解读
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