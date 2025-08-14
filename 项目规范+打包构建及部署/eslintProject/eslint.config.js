// import js from "@eslint/js";
// import globals from "globals";
// import pluginVue from "eslint-plugin-vue";
// import { defineConfig } from "eslint/config";

// export default defineConfig([
//   { files: ["**/*.{js,mjs,cjs,vue}"], plugins: { js }, extends: ["js/recommended"], languageOptions: { globals: globals.browser } },
//   pluginVue.configs["flat/essential"],
// ]);
import tsParser from '@typescript-eslint/parser'
import vueParser from 'vue-eslint-parser'
import {eslintChinesePlugin} from './eslint/plugins/eslint-plugin-chinese.js'
export default{
  files:['**/*.ts','**/*.vue'],
  ignores:['eslint.config.js'],
  languageOptions:{
    parser:vueParser,
    parserOptions:{
      parser:tsParser
    }
  },
  plugins:{
    'chinese':eslintChinesePlugin // 插件注册，插件的名称就是规则的作用域rules:{'chinese/no-chinese-vars':"error"}
  },
  rules:{
    "no-unused-vars":"error", // 不允许声明没有使用的变量
    "no-console":"error",// 不允许打印console
    "no-sparse-arrays":"error", // 不允许组数定义的时候有多余的逗号
    "no-undef":"error", // 不允许未声明的变量
    "no-unreachable":"error", // 不允许函数return后还写代码
    "no-dupe-keys":"error", // 不允许对象有重复的key
    "chinese/no-chinese-vars":"error"
  }
}