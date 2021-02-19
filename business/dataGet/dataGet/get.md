# 数据采集
## 一：什么是数据采集
    数据采集是为了满足挖掘，统计，分析的需求，来获取和收集各种数据的过程。
## 二：数据采集的应用场景：
    个性化推荐，搜索优化，精准广告，在线分析，用户画像，文本挖掘等。
## 三：常见的数据采集目标：
    1.按照类型分类包括：用户行为数据（点击，APP启动，表单提交等行为），用户数据（如APP注册信息，微信第三方授权用户信息等），业务数据（如商品支付，退款等），内容数据
    2.按照所有者分类：第一方数据，第三方数据（如接入的第三方页面）
## 三：数据采集的原则
    1.大：充分考虑用户规模和数据规模的增长，做好资源积累工作，
    2.全：多端采集，尽量针对全量用户行为而非单个用户。
    3.细：尽量采集足够多的属性和维度，如从who,when,how,where,what这五个维度来采集用户数据。
    4.时：尽可能提高数据采集的时效性。
## 四：数据采集的方式
##### 1.代码埋点
    (1)什么是代码埋点？
        在某个控件操作发生时通过预先写好的代码来发数据的方式称为代码埋点，如输入框失去焦点时发送输入框中的数据。
    (2)代码埋点的优势和劣势
        优点:
            能够精确控制埋点位置。
            可以方便灵活地自定义事件，自定义属性。
            采集的数据更丰富。
            可以满足更精细化的需求。
        缺点：
            埋点代价较大，更新迭代实现较为困难：每个控件都需要添加相应的埋点代码，每次埋点方案更新时都需要改代码，然后APP更新等。
            前端数据埋点存在传输时效性，可靠性等方面的问题，该问题只能依靠后端埋点解决。
    (3)实现流程：APP或页面初始化 ---> 初始化第三方数据分析服务商的SDK ---> 事件发生时调用SDK中的接口发送数据
##### 2.可视化埋点
    （1）什么叫可视化埋点？
        当使用者在后台的截屏画面上点击了某个可埋点的控件时，后台会要求使用者做一些事件关联方面的配置，并且将配置信息进行保存和部署。
        通过可视化界面配置控件操作与事件发生关系的可视化埋点
##### 3.全埋点
    (1)什么是全埋点？
        全埋点：也叫做无痕埋点，自动埋点，无埋点。这种方式是通过预先尽可能多的收集控件的操作数据，即用户的行为数据，它仅能采集一些最标准的数据。
    (2)全埋点支持的事件：
        激活(APP安装后的首次启动);
        APP启动（即APP唤醒，包括冷启动和热启动，通常需要注意启动的来源等）;
        APP退出(使用时长，退出方式（home键），跳转到其他APP，APP crash， 强杀等等);
        APP页面浏览（自定义属性，页面标题，前向页面，android，ios，页面名称）;
        APP控件点击;
        曝光（曝光的定义方式，常见曝光：广告位，列表，对话框等）;
        crash;
## 五：数据采集方案的选择：
    1.在确定数据采集方案时应该遵循的两个基本原则：
        优先在后端收集数据；
        属性尽可能采集全面。
        因为前端埋点存在一些问题：如需要等待网络良好时才能发送数据，数据需要本地暂存，但本地暂存空间有限，数据传输时容易丢失等，然而我们仍需要前端埋点。
    2.前端埋点方案对比：
        “无埋点”相比可视化埋点的优点：
            1.解决了数据“回溯”的问题，例如，在某一天，突然想增加某个控件的点击的分析，如果是可视化埋点方案，则只能从这一时刻向后收集数据，而如果是“无埋点”，则从部署  SDK 的时候数据就一直都在收集了；
            2.“无埋点”方案也可以自动获取很多启发性的信息，例如，“无埋点”可以告诉使用者这个界面上每个控件分别被点击的概率是多大，哪些控件值得做更进一步的分析等等。
        缺点：
            1.覆盖的功能有限；
            2.无法自动采集业务相关的数据；
            3.无法满足更精细化的分析需求；
            4.存在兼容性问题；
            5.传输的数据量太大，浪费资源，给服务器和网络添加了负担。
        
## 六：神策埋点sa-sdk-javascript应用,将其作为一个开发插件来提供全局功能：


api文件配置
```js
// 引入神策sdk
import sensors from 'sa-sdk-javascript'
/*
*Vue的插件暴露一个install方法
*参数一：Vue实例
*参数二：options,可选的配置对象
*/
export default function install(Vue, options) {
  // sensors对象本身存在一些属性用于埋点等业务功能
  // 挂在vue实例下
  Vue.prototype.$sensors = sensors

  // 注册全局属性，sensors.registerPage()方法需要在初始化sdk之后，开启全埋点之前添加
  sensors.registerPage({
    current_url: location.href,
    referrer: document.referrer
  })


  // 开启全埋点
  sensors.init({
    server_url: 'http://test-syg.datasink.sensorsdata.cn/sa?token=xxxxx&project=xxxxxx',
    is_track_single_page:true, // 单页面配置，默认开启，若页面中有锚点设计，需要将该配置删除，否则触发锚点会多触发 $pageview 事件
    use_client_time:true, 
    send_type:'beacon',
    heatmap: {
      //是否开启点击图，default 表示开启，自动采集 $WebClick 事件，可以设置 'not_collect' 表示关闭。
      clickmap:'default',
      //是否开启触达注意力图，not_collect 表示关闭，不会自动采集 $WebStay 事件，可以设置 'default' 表示开启。
      scroll_notice_map:'default'
    } 
  })
  sensors.quick('autoTrack')

  /*
  *sensors.track()方法用于追踪用户行为事件，并添加自定义属性
  *参数一：自定义行为事件名称
  *参数二：自定义属性
  */
  sensors.track('BuyProduct', {
    ProductName: "MacBook Pro", 
    ProductPrice: 123.45, 
    IsAddedToFav: false,
  })
  
  // 也可以在sensors对象下添加一些方法,注：添加click，visit方法是为了区分埋点来源属于点击事件或者页面访问事件，也可以不区分直接使用track()方法
  sensors.click = function (data, type = 'BXClick') {
    const option = Object.assign({}, defaultOption, data)
    return sensors.track(type, option)
  }
  sensors.visit = function (data, type = 'BXClick') {
    const option = Object.assign({}, defaultOption, data)
    return sensors.track(type, option)
  }
}
```

main.js文件配置
```js
import SaApi from '@/api/sa' // 引入插件所在文件
Vue.use(SaApi) // 使用插件
```


具体页面使用
```js
<template>
</template>
<script>
created () {
  this.$sensors.visit({'content': 'test埋点内容'})
  this.$sensors.track({'content': 'test埋点内容'})
}
</script>
```