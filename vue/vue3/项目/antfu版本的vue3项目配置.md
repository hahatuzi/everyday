# eslint9,prettier,husky,commitlint
# 全新搭建配置,采用github上antfu的方案
  ### npm create vue
  ### 不使用eslint,prettier相关插件,因为后面会使用antfu的prettier和eslint
  ### stylelint使用
   - vscode安装stylelint插件
   - 安装stylelint相关插件，npm i sass postcss postcss-html postcss-scss stylelint stylelint-config-recess-order stylelint-config-standard -D
   - 配置stylelint.config.mjs文件
  ### antfu组合prettier和eslint
   - npx @antfu/eslint-config@latest
   - package.json添加脚本
     ```js
     "scripts": {
        "lint":"eslint .",
        "lint:fix": "eslint . --fix",
        "lint:stylelint": "stylelint --cache \"**/*.{css,scss,vue}\" --fix",
      },
     ```
   - 按照提示一直执行，然后就会发现文件保存的时候可以自动格式化了
   - 还可以添加stylelintignore忽略文件
     ```js
      dist
      node_modules
      public
      .husky
      .vscode
      .idea
      *.sh
      *.md
     ```
  ### 代码提交检查：Husky,lint-staged,commitlint,commitizen,cz-git配置git提交代码规范