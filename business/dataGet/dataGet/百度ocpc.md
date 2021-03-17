# 本笔记为了记录前端方面实现百度OCPC转化数据对接的代码。承接上文中的数据追踪技术选型。
上文中的百度数据追踪技术为百度统计，本文涉及内容为百度OCPC
## 一：什么是转化数据对接？
转化数据对接是指广告主通过某种将广告产生的转化数据回传给百度，从而通过百度进行深度数据分析的过程。
## 二：百度OCPC的技术应用场景（仅从技术方面考虑）：
1.JS方面：面向web开发
2.小程序方面：
3.APP：面向投放APP的客户，比如引导APP下载
4.API：面向有API开发能力的客户，广告主可以自己转化归因，及分析数据转化。
5.基木鱼：面向落地页是基木鱼的客户，百度自己收集数据，基木鱼是指百度给广告主生成落地页，因为是百度自己生成的落地页所以百度可以自己收集数据，个人从项目及业务方面考虑，并不推荐该方法
6.BCP:面向已接入第三方咨询工具的客户，收集咨询类转化
## 三：JS方面的技术实现及方案选型：
注：通过以上二中的技术应用场景分析，本次仅考虑前端应用最多的JS方面的技术实现
#### 1.成功类转化行为埋码：（针对转换类型为表单提交成功的情况）
```js
// sdk安装 ---> 在表单提交成功后的代码中添加代码：window._agl && window._agl.push(['track', ['success', { t: 3 }]])
```
#### 2.点击类转换属性埋码：（针对网页点击等情况）
```js
// sdk安装 ---> 设置转化属性：data-agl-cvt，具体属性值参考属性转码表
// 如：
<button data-agl-cvt="6"></button>
```
#### 3.微信复制类（微信加粉）
```js
// sdk安装 ---> 基于以上1，2中的成功类转化或点击类转化实现（因为第一步中的sdk无法监听到“长按复制”这种交互行为）
// 如借助clipboardjs
<span v-clipboard:copy="wechat_id" v-clipboard:success="clipboardSuccess"></span>
clipboardSuccess () {
    window._agl && window._agl.push(['track', ['success', { t: 3 }]])
    alert('复制成功')
}
```
注：不管是选择以上三种类型中的哪一种，均需要先进行sdk基础代码安装
```js
<script>
    window._agl = window._agl || [];
    (function () {
        _agl.push(
            ['production', '_f7L2XwGXjyszb4d1e2oxPybgD'] // production值唯一，所有客户共用同一值，百度根据数据来源自动区分不同客户
        );
        (function () {
            var agl = document.createElement('script');
            agl.type = 'text/javascript';
            agl.async = true;
            agl.src = 'https://fxgate.baidu.com/angelia/fcagl.js?production=_f7L2XwGXjyszb4d1e2oxPybgD';
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(agl, s);
        })();
    })();
</script>
```