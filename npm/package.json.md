{
  "name": "ruoyi",// 项目名称
  "version": "3.8.3",// 项目版本号
  "description": "",
  "author": "若依",
  "license": "MIT",
  "private":"true",// 当前项目是否私有化
  "scripts": {
    "dev": "vue-cli-service serve",
    "build:prod": "vue-cli-service build",
    "build:stage": "vue-cli-service build --mode staging",
    "preview": "node build/index.js --preview",
    "lint": "eslint --ext .js,.vue src"
  },
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "src/**/*.{js,vue}": [
      "eslint --fix",
      "git add"
    ]
  },
  "keywords": [
    "vue",
    "admin",
    "dashboard",
    "element-ui",
    "boilerplate",
    "admin-template",
    "management-system"
  ],
  "repository": {
    "type": "git",
    "url": "https://gitee.com/y_project/RuoYi-Vue.git"
  },
  "dependencies": {
    "@riophae/vue-treeselect": "0.4.0",
    "axios": "0.24.0",
    "clipboard": "2.0.8",
    "core-js": "3.19.1",
    "echarts": "4.9.0",
    "element-ui": "2.15.8",
    "file-saver": "2.0.5",
    "fuse.js": "6.4.3",
    "highlight.js": "9.18.5",
    "js-beautify": "1.13.0",
    "js-cookie": "3.0.1",
    "jsencrypt": "3.0.0-rc.1",
    "nprogress": "0.2.0",
    "quill": "1.3.7",
    "screenfull": "5.0.2",
    "sortablejs": "1.10.2",
    "vue": "2.6.12",
    "vue-count-to": "1.0.13",
    "vue-cropper": "0.5.5",
    "vue-meta": "2.4.0",
    "vue-router": "3.4.9",
    "vuedraggable": "2.24.3",
    "vuex": "3.6.0"
  },
  // devDev属性中的包仅在开发环境需要，一些包在生产环境不需要比如webpack,babel
  "devDependencies": {
    "@vue/cli-plugin-babel": "4.4.6",
    "@vue/cli-plugin-eslint": "4.4.6",
    "@vue/cli-service": "4.4.6",
    "@vue/compiler-sfc": "^3.2.41",
    "babel-eslint": "10.1.0",
    "babel-plugin-dynamic-import-node": "2.3.3",
    "chalk": "4.1.0",
    "compression-webpack-plugin": "5.0.2",
    "connect": "3.6.6",
    "eslint": "7.15.0",
    "eslint-plugin-vue": "7.2.0",
    "lint-staged": "10.5.3",
    "runjs": "4.4.2",
    "sass": "1.32.13",
    "sass-loader": "10.1.1",
    "script-ext-html-webpack-plugin": "2.1.5",
    "svg-sprite-loader": "5.1.1",
    "uglifyjs-webpack-plugin": "^2.2.0",
    "vue-template-compiler": "2.6.12"
  },
  "engines": {
    "node": ">=8.9",
    "npm": ">= 3.0.0"
  },
  // browserslist用于配置打包后的JS浏览器的兼容情况
  "browserslist": [
    "> 1%",
    "last 2 versions"
  ]
}