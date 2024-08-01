# 一：从URL到页面渲染
  ### 第一步：浏览器进程对域名进行解析，然后将URL请求派发给网络进程
    包括对协议，域名，路径，参数等进行解析，域名解析就是将域名解析成IP，然后从本机开始由近及远的查询域名内容
  ### 第二步：DNS查询
    查询浏览器或者操作系统缓存中是否已经有对应域名的访问记录，有的话直接使用缓存
  ### 第三步：网络进程建立TCP连接
    **TCP三次握手原理**
  ### 第四步：网络进程发送http请求
    请求包含请求头，请求体，等信息
  ### 第五步：服务器响应，然后网络进程将数据转发给浏览器主进程
    响应信息包含响应数据，响应头等
  ### 第六步：浏览器主进程边响应边解析，然后发送“提交文档”给渲染进程
  包含解析HTML，CSS，执行JS
  ### 第七步：然后渲染进程渲染，渲染完毕后通知主进程渲染完成
    先将解析的DOM和CSS,JS合并成渲染树，再形成排列页面布局，最后绘制元素，此处注意**重绘重排**
    其中<link>标签，图片，视频等资源不会阻塞渲染，<script>包含影响DOM的方法，会阻塞渲染
    
# 二：script相关问题
  ### 1.script是否会阻塞html渲染，阻塞了什么东西
    script阻塞了DOM解析，js执行，从而阻塞了浏览器渲染
  ### 2.async和defer和同步js的下载顺序
    - <script>包含影响DOM的方法，会阻塞渲染
    - <script defer> **延迟**，异步请求获取该脚本文件，不会影响后续DOM的渲染，会先**等html解析完毕后再执行该js脚本**
    - <script async> **异步**，也是异步请求获取该脚本文件，不会阻塞浏览器解析html，当它**异步数据返回后会中断解析html，执行相关的js**
    - <script type="module">按需加载
    - <script>标签内容执行完毕后会触发DOMContentLoaded事件
  ### 3.async和defer的区别
  ### 4.async和defer的混合执行顺序
    多个async时不确定，因为异步脚本执行时长不一样，多个defer时会按照顺序执行
  ### 5.async和defer和DOMContentLoaded回调函数的执行顺序
     - DOMContentLoaded会在defer script执行完毕后执行，与async script无关
  ### 6.defer和async的使用场景
   - 当某个js脚本对首屏渲染没有任何影响时，加个defer，反正会在html都解析完毕后才执行该js，
   - 当用户下拉内容时，页面稳定后，还有100个毫不相关的script渲染100个模块，如使用defer，defer会在100个script下载完毕后才执行，用户如果已经开始翻动，则后面都是白屏，体验是较差的。这时改为async，用户在翻动时会看到最先渲染出来的异步模块，像极了懒加载，体验比defer更好些。
    |         script          |       js执行顺序       |  是否阻塞解析html    |
    | ----------------------- | -----------------------| ---------------------|
    |          <script>       |    按html顺序执行      |         阻塞         |
    |      <script async>     |    按请求返回顺序      |        可能阻塞      |
    |      <script defer>     |    按html顺序执行      |        不阻塞        |

# 三：渲染进程的详细渲染流程
  ### （1）使用**html解析器**将html页面转换成DOM树，ParseHTML
  ### （2）将css解析成CSS树，ParserCSS
  - 如果css样式没有通过link标签引入，样式还是会通过html解析器解析。
  - **link会阻塞浏览器的渲染**，因为本质上link解析也是浏览器解析的一部分，但**不会阻塞DOM解析**。
  - CSS文件的引入如果放在底部会阻塞DOM渲染。
  ### （3）计算DOM树每个节点的具体样式,Attachment
  ### （4）DOM树+ CSS树 --> 布局树 
  ### （5）根据布局树生成图层树 update LayerTree
  ### （6）绘制图层 paint
  ### （7）组合图层
  - 图层树：什么样的场景可以生成图层树呢？打开调试工具的layers工具就可以看到图层树
  添加css 3d的元素，position:fixed的元素，video标签，canvas,css3动画
# 四：重绘重排
  - layout为重排，重排就是**回流**。
    - 更新元素的**几何属性**，**计算所有元素在窗口的位置,**。当添加，删除元素，修改大小，位置等时会触发
  - repaint为重绘。
    - 更新元素的**绘制属性**重新**计算所有元素在窗口具体呈现的内容**，比如改变背景颜色。
    重绘重排是以图层为单位进行的,
    重排一定触发重绘，但重绘不一定会触发重排。

# 五：performance API
  ### :,
|   时间节点  |              描述              |                             含义                          |
| ----------- | -------------------------------| ----------------------------------------------------------|
|      TTFB   |       time to first byte       |             从请求到数据返回第一个字节所消耗的时间        |
|      TTI    |      time to interactive       |              DOM树构建完毕，代表可以绑定事件              |
|      DCL    |         domContentLoaded       |   当html文档被完全加载和解析完成后触发domContentLoaded    |
|       L     |               onLoad           |                  依赖资源全部加载完毕后触发               |
|      FP     |            first paint         |               首次绘制，第一个像素点绘制到屏幕的时间      |
|      FCP    |    first contentful Paint      |                     首次绘制任何内容的时间                |
|      FMP    |    first meaningful paint      |           首次有意义的绘制，它是衡量页面可用性的标准      |
|      LCP    |   largest contentfule paint    |             viewport中最大的页面元素加载的时间            |
|      FID    |         first input delay      |             用户首次和页面交互到页面响应的时间            |