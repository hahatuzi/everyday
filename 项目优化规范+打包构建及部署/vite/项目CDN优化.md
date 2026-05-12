# 哪些资源可以放在CDN服务器上
1.体积较大的非业务js文件，比如react,react-dom
2.非业务js文件，不需要经常变动，CDN不用频繁更难缓存
# 做法：
```js
const {whenProd, getPlugin, pluginByName} = require('@/craco/craco')
configure:(webpackConfig) => {
  let cdn
  whenProd(() => {
    webpackConfig.externals = {
      react:'React',
      'react-dom':'ReactDOM'
    }
    cdn = {
      js:[
        'https://cdnjs.cloudflare.com/ajax/libs/react/18.1.0/umd/react.production.',
        'https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.1.0/umd/react-dom.production.',
      ]
    }
  })
  const {isFound, match} = getPlugin(
    webpackConfig,
    pluginByName('HtmlWebpackPlugin')
  )
  if (ifFound) {
    match.userOptions.cdn = cdn
  }
  return webpackConfig
}
// 在index..tml中动态插入cdn资源url
<% htmlWebpackPlugin.options.cdn.js.forEach(cdnURL => { %>
<script src="<%= cdnURL %>"></script>
<% }) %>
```