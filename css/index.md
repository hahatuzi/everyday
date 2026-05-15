# 一：元素定位的相关知识复习：
  ### 1.relative的基本原理复习，以及relative定位的盒子给其他元素带来的影响
  - relative定位的盒子是相参照自身本来的位置来改变的，不影响后续其他的标准流的元素
    ```js
      <style>
      .relative{
          position：relative;
          left:20px;
      }
      </style>
      <div class="relative"></div>
      <div></div>
    ```
  ### 2.absolute绝对定位到底依赖谁？
  - absolute定位的元素相对于自己有定位的最近祖先元素。只要祖先元素有定位即可(relitive,absolute均可),若父元素没有定位则以浏览器为准。
  ### 3.fixed定位和sticky定位到底依赖谁。fixed固定定位的盒子，相对于浏览器的可视化窗口来说的

# 二：伪类选择器：a:link; a:visited; a:hover; a:active
  - 为了符合浏览器解析CSS所遵循的就近原则，将一般的放在上面，将特殊的放在下面。**hover必须放在link和visited后面，active之前**

# 三：div的几种隐藏方式：
  - 1.display:none
  - 2.visibility:hidden
  - 3.background-color:transparent
  - 4.opacity:设置不透明度
  - 5.给div一个margin负值再结合使用overflow：hidden
  - 6.将div的width和height设置为0
  - 7.利用定位：子绝父相，并给子元素left值为自身宽度。

# 四：background的一些属性
  ### 1.background-position:
  - 若想要背景图片在盒子的右下角20%处的写法：background-position: right 20% bottom 20%;
  -  超大背景图片的位置为：background-position: center top;
  ### 2.background-size的cover和contain的区别
  - cover:缩放背景图片以完全覆盖背景区（当容器和背景图大小不同时，背景图的 左/右 或者 上/下 部分会被裁剪）。
  - contain:缩放图片完全装入背景区域内，（当背景图和容器的大小的不同时，容器的空白区域（上/下或者左/右）会显示空白）。

# 五：CSS控制图片HTTP请求的情形实例解析：
  ### 1.作为img标签
  - （1）display：none属性控制，除opera外均会发生请求
  - （2）visibility:hidden，均产生请求
  ### 2.作为背景图片，挂靠元素不存在的时候不发送请求，以下仅考虑存在的情况
  - （1）display:none，Opera和Firefox对于用display: none隐藏的元素背景，不会产生HTTP请求
  - （2）visibility:hidden
  - （3）多重背景图时：CSS写法时：只会请求最后一次，前面的都会被覆盖
    ```js
      <style>
      .test{
          background:url('1')
      }
      .test{
          background:url('2')
      }
      </style>
      <div class="test"></div>
      ```
      CSS3写法时：webkit引擎会都请求，因为支持c3写法
      ```js
      <style>
      .test{
          background-image:url('1'),url('2')
      }
      </style>
      <div class="test"></div>
    ```

# 六：滚动时的属性
  - scroll-snap-stop
  - scroll-snap-align
  - scroll-snap-type

# 七：选择器大全
  - 后代选择器：div.wrap .demo
  - 子元素选择器 .wrap>.demo
  - 相邻兄弟选择器 div.wrap+.demo
  - nth-child,nth-of-type

# 八：移动端会出现软键盘弹出时fixed定位的元素被顶上去的问题。
  - 产生原因，键盘弹起时会引起窗口高度html标签的高度的改变，而fixed定位是相对于html元素的，所以会被顶上去。

# 九：flex:1和flex:auto的区别
  ### 1.三个基本属性
   - **flex-grow**:项目的增长系数，项目在剩余空间的相对比例：默认为0，即如果存在剩余区域，该项目会放大。
   - **flex-shrink**:项目的收缩规则：默认为1，即如果可分配空间不足，会适当缩小项目。
   - **flex-basis**:在分配空间之前，项目的主轴空间，相当于我们设置的width
  ### 2.flex的三种情况的区别
   - flex:none
   - flex:1
   - flex:auto
    ```js
      // flex:none: // flex: 0 0 auto;表示项目不会伸缩，保持原始大小
      // flex:1:  // flex: 1 1 0%;
      // flex:auto: // flex: 1 1 auto;表示项目会根据自身大小和剩余空间进行缩放
        // 如果width和flex-basis同时设置，非auto的flex-basis权重更大
        <div class="flex-box">
            <div class="item1">短文本</div>
            <div class="item2">文本内容一定要比item长，文本内容一定要比item长</div>
        </div>

        <style type="text/css">
            .flex-box{
         display: flex;
              width: 1000px;
              text-algin:center;
          }

          .item1 {
              height: 100px;
              flex: 1 1 0%; /*flex-basis为0%，覆盖width，实际占用0*/
              background:red;
          }

          .item2 {
              height: 100px;
              width: 400px;
              flex: 1 1 auto;  /*flex-basis为auto，width权限更高，占用300*/
              background:green;
          }
          /* 分配宽度前：
          字元素占用空间为：0+400
          可分配空间：600
          放大比例：1:1，获取的可放大空间：300+300
          */
          /* 实际子元素空间：
          0+300
          400+300
          */
      </style>
    ```

# 十：image的属性大全
  ### 1.pointer-events：auto/none
  指定情况下图形元素可以变成鼠标事件，为**防止在APP等内图片点击变成预览**效果，需要将pointer-events:none
  ### 2.垂直居中div内的一张img
    ```js
      div{
          line-height:200px;
          img{
              vertical-align: middle
          }
      }
    ```

# 十一：同一个元素不能同时应用transform属性和animate属性。
  - 解决方法：将其中一个属性应用至父级元素。
    ```js
      <div>
        <img src="">
      </div>
      div{
          position:absolute;
          left:50%;
          transfrom:translate(-50%);
          // 可将transform和animate其中一个属性应用至父级元素上
          img{
              animate:breathe 2s infinite;
          }
      }
      @keyframe breathe{
          0%{
              transform:scale(1);
          }
          50%{
              transform:scale(0.8);
          }
          100%{
              transform:scale(1);
          }
      }
    ```
# 十二：line-height:120%和line-height：1.2的区别
  line-height:1.2可以继承，即使子元素有自己的font-size，但是子元素的行高仍然不是自己的font-size的高度，而是继承自父元素的1.2*自己的font-size