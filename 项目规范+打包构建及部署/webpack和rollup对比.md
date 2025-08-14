# 打包对比
webpack是将commonjs转化为模块化代码，rollup是基于ESM的JavaScript打包工具，ESM比CommonJS模块机制更高效。
且rollup打包后的可读性更好，因为rollup的tree shaking.

- rollup的transform插件相当于webpack的loader
Rollup使用新的ESM，而Webpack用的是旧的CommonJS。
Rollup 的打包文件体积很小。
Rollup支持相对路径，webpack需要使用path模块。
尽管esbuild速度更快，但Vite采用了Rollup灵活的插件API和基础建设，这对Vite在生态中的成功起到了重要作用。

[!参考链接]https://juejin.cn/post/7240740177449435191