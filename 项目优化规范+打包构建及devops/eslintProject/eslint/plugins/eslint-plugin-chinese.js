import { noChineseVars } from '../rules/no-chinese-vars.js'

export const eslintChinesePlugin = {
  rules:{
    "no-chinese-vars":noChineseVars // 规则的具体实现
  }
}